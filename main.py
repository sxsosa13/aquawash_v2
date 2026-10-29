"""Acceso a datos y reglas de negocio de Sosa Car Wash (compartido por escritorio y web)."""
import hashlib
import os
from contextlib import contextmanager
from datetime import date

import psycopg2
import psycopg2.errors
import psycopg2.extras
import psycopg2.sql

from config import DB_CONFIG, HORARIOS, PUESTOS_SIMULTANEOS


@contextmanager
def conexion():
    con = psycopg2.connect(**DB_CONFIG)
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def consultar(sql, params=None):
    with conexion() as con, con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def ejecutar(sql, params=None):
    with conexion() as con, con.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()[0] if cur.description else None


def mensaje_error(e):
    if isinstance(e, UnicodeDecodeError):
        return e.object.decode("cp1252", errors="replace")
    return str(e)


def hash_clave(clave, sal=None):
    sal = sal or os.urandom(8).hex()
    h = hashlib.pbkdf2_hmac("sha256", clave.encode(), sal.encode(), 100_000).hex()
    return f"{sal}${h}"


def verificar_clave(clave, guardada):
    sal = guardada.split("$")[0]
    return hash_clave(clave, sal) == guardada


def autenticar(usuario, clave):
    filas = consultar("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    if filas and verificar_clave(clave, filas[0]["clave"]):
        return filas[0]
    return None


def asegurar_base():
    con = psycopg2.connect(**dict(DB_CONFIG, dbname="postgres"))
    try:
        con.autocommit = True
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_CONFIG["dbname"],))
            if not cur.fetchone():
                cur.execute(psycopg2.sql.SQL("CREATE DATABASE {}").format(
                    psycopg2.sql.Identifier(DB_CONFIG["dbname"])))
    finally:
        con.close()


def inicializar():
    asegurar_base()
    ruta = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(ruta, encoding="utf-8") as f:
        ejecutar(f.read())
    try:
        ejecutar("CREATE INDEX idx_citas_fecha ON citas (fecha, hora)")
    except psycopg2.errors.DuplicateTable:
        pass
    if not consultar("SELECT 1 FROM usuarios LIMIT 1"):
        ejecutar("INSERT INTO usuarios (usuario, clave, nombre, rol) VALUES (%s, %s, %s, 'ADMIN')",
                 ("admin", hash_clave("admin123"), "Administrador"))
        ejecutar("INSERT INTO usuarios (usuario, clave, nombre, rol) VALUES (%s, %s, %s, 'OPERADOR')",
                 ("operador", hash_clave("operador123"), "Operador de turno"))
    if not consultar("SELECT 1 FROM servicios LIMIT 1"):
        for datos in [("Lavado básico", "AUTO", 100000, 45), ("Lavado completo", "AUTO", 180000, 90),
                      ("Lavado + encerado", "AUTO", 260000, 120), ("Lavado de moto", "MOTO", 70000, 30),
                      ("Lavado + lubricación de cadena", "MOTO", 120000, 45)]:
            ejecutar("INSERT INTO servicios (nombre, tipo_vehiculo, precio, duracion_min) VALUES (%s, %s, %s, %s)", datos)


def horarios_disponibles(fecha):
    date.fromisoformat(fecha)
    filas = consultar("SELECT hora, COUNT(*) AS n FROM citas WHERE fecha = %s AND estado <> 'CANCELADA' GROUP BY hora", (fecha,))
    ocupados = {f["hora"].strftime("%H:%M"): f["n"] for f in filas}
    return [h for h in HORARIOS if ocupados.get(h, 0) < PUESTOS_SIMULTANEOS]


def crear_cita(vehiculo_id, servicio_id, fecha, hora, origen="ESCRITORIO", observacion=""):
    if date.fromisoformat(fecha) < date.today():
        raise ValueError("No se puede agendar en una fecha pasada.")
    if hora not in horarios_disponibles(fecha):
        raise ValueError("Ese horario ya no tiene puestos disponibles.")
    v = consultar("SELECT tipo FROM vehiculos WHERE id = %s", (vehiculo_id,))
    s = consultar("SELECT tipo_vehiculo FROM servicios WHERE id = %s AND activo", (servicio_id,))
    if not v or not s:
        raise ValueError("Vehículo o servicio no válido.")
    if v[0]["tipo"] != s[0]["tipo_vehiculo"]:
        raise ValueError("El servicio elegido no corresponde al tipo de vehículo.")
    return ejecutar("INSERT INTO citas (vehiculo_id, servicio_id, fecha, hora, origen, observacion) "
                   "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                   (vehiculo_id, servicio_id, fecha, hora, origen, observacion or None))


def reserva_web(d):
    for campo in ("nombre", "telefono", "placa", "tipo", "servicio_id", "fecha", "hora"):
        if not str(d.get(campo, "")).strip():
            raise ValueError(f"Falta completar el campo: {campo}.")
    if d["tipo"] not in ("AUTO", "MOTO"):
        raise ValueError("Tipo de vehículo inválido.")
    placa = d["placa"].strip().upper()
    fila = consultar("SELECT id FROM vehiculos WHERE placa = %s", (placa,))
    if fila:
        vehiculo_id = fila[0]["id"]
    else:
        cliente_id = ejecutar("INSERT INTO clientes (nombre, telefono, email) VALUES (%s, %s, %s) RETURNING id",
                              (d["nombre"].strip(), d["telefono"].strip(), d.get("email") or None))
        vehiculo_id = ejecutar("INSERT INTO vehiculos (cliente_id, tipo, placa) VALUES (%s, %s, %s) RETURNING id",
                               (cliente_id, d["tipo"], placa))
    return crear_cita(vehiculo_id, int(d["servicio_id"]), d["fecha"], d["hora"], "WEB",
                      d.get("observacion", ""))


def cobrar_cita(cita_id, metodo):
    with conexion() as con, con.cursor() as cur:
        cur.execute("SELECT s.precio, c.estado FROM citas c JOIN servicios s ON s.id = c.servicio_id WHERE c.id = %s", (cita_id,))
        monto, estado = cur.fetchone()
        if estado in ("COMPLETADA", "CANCELADA"):
            raise ValueError(f"La cita ya está {estado.lower()}.")
        cur.execute("INSERT INTO pagos (cita_id, monto, metodo) VALUES (%s, %s, %s)",
                    (cita_id, monto, metodo))
        cur.execute("INSERT INTO ingresos (fecha, detalle, monto, categoria) VALUES (%s, %s, %s, %s)",
                    (date.today(), f"Servicio cita #{cita_id}", monto, "SERVICIO"))
        cur.execute("UPDATE citas SET estado = 'COMPLETADA' WHERE id = %s", (cita_id,))
    return monto


def ingresos_por_dia(desde, hasta):
    return consultar("SELECT fecha::date AS dia, SUM(monto) AS total FROM ingresos WHERE fecha::date BETWEEN %s AND %s GROUP BY 1 ORDER BY 1", (desde, hasta))


def egresos_por_dia(desde, hasta):
    return consultar("SELECT fecha::date AS dia, SUM(monto) AS total FROM egresos WHERE fecha::date BETWEEN %s AND %s GROUP BY 1 ORDER BY 1", (desde, hasta))


def servicios_top(desde, hasta):
    return consultar("SELECT s.nombre, COUNT(*) AS cantidad FROM citas c JOIN servicios s ON s.id = c.servicio_id WHERE c.fecha BETWEEN %s AND %s AND c.estado <> 'CANCELADA' GROUP BY s.nombre ORDER BY cantidad DESC", (desde, hasta))


def listar_insumos():
    return consultar("SELECT * FROM insumos WHERE activo ORDER BY nombre")


def registrar_insumo(nombre, categoria, cantidad, unidad, costo_unitario, stock_minimo=0):
    nombre = nombre.strip()
    if not nombre:
        raise ValueError("El nombre del insumo es obligatorio.")
    return ejecutar("INSERT INTO insumos (nombre, categoria, cantidad, unidad, costo_unitario, stock_minimo) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                   (nombre, categoria or "GENERAL", cantidad, unidad or "unidad", costo_unitario, stock_minimo))


def actualizar_insumo(insumo_id, nombre, categoria, cantidad, unidad, costo_unitario, stock_minimo=0):
    return ejecutar("UPDATE insumos SET nombre=%s, categoria=%s, cantidad=%s, unidad=%s, costo_unitario=%s, stock_minimo=%s, actualizado=NOW() WHERE id=%s",
                   (nombre.strip(), categoria or "GENERAL", cantidad, unidad or "unidad", costo_unitario, stock_minimo, insumo_id))


def insumos_bajo_stock():
    return consultar("SELECT * FROM insumos WHERE activo AND cantidad <= stock_minimo ORDER BY nombre")


def registrar_egreso(fecha, detalle, monto, categoria="OPERATIVO"):
    return ejecutar("INSERT INTO egresos (fecha, detalle, monto, categoria) VALUES (%s, %s, %s, %s) RETURNING id",
                   (fecha, detalle.strip(), monto, categoria))


def balance_economico(desde, hasta):
    ingreso = consultar("SELECT COALESCE(SUM(monto), 0) AS total FROM ingresos WHERE fecha BETWEEN %s AND %s", (desde, hasta))[0]["total"]
    egreso = consultar("SELECT COALESCE(SUM(monto), 0) AS total FROM egresos WHERE fecha BETWEEN %s AND %s", (desde, hasta))[0]["total"]
    return {"ingresos": float(ingreso), "egresos": float(egreso), "balance": float(ingreso - egreso)}


def registrar_contacto(nombre, telefono, email, mensaje):
    return ejecutar("INSERT INTO contacto (nombre, telefono, email, mensaje) VALUES (%s, %s, %s, %s) RETURNING id",
                   (nombre.strip(), telefono.strip() if telefono else None, email.strip() if email else None, mensaje.strip() if mensaje else None))
