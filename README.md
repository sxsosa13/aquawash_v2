# AquaWash · Gestión de lavadero de autos y motos

Python 3 · Tkinter · PostgreSQL · Página web de reservas · Todo administrable desde Visual Studio Code

## 1. Requisitos (instalar una sola vez)
1. **Python 3.10+** (marque *Add Python to PATH*). En Linux: `sudo apt install python3-tk`.
2. **PostgreSQL 9.3 o superior** (el servidor de base de datos). Anote la contraseña del usuario `postgres`.
   *Alternativa sin instalar:* con Docker, `docker compose up -d` (contraseña: `postgres`).
3. **Visual Studio Code** (https://code.visualstudio.com).

## 2. Abrir el proyecto
1. Descomprima `aquawash.zip`.
2. En VS Code: **Archivo > Abrir carpeta…** y elija la carpeta `aquawash`
   (o abra el archivo `aquawash.code-workspace`).
3. Acepte la sugerencia **«Instalar extensiones recomendadas»**: *Python*, *SQLTools* y *SQLTools PostgreSQL Driver*.

## 3. Preparar el entorno (terminal de VS Code: Ctrl+ñ)
```
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```
Si VS Code pregunta por el intérprete, elija el de `venv`.

## 4. Crear la base de datos desde VS Code (sin pgAdmin)
Pulse **F5** y elija **«AquaWash · 1) Configurar base de datos (primera vez)»**.
El asistente, en la terminal de VS Code:
1. Le pide servidor, puerto, usuario y **contraseña de PostgreSQL**.
2. Prueba la conexión y le explica el error si falla.
3. Crea la base `aquawash`, las 6 tablas, los usuarios y los servicios iniciales.
4. Le ofrece cargar datos de ejemplo.

La conexión queda guardada en `config_local.json` (no necesita editar `config.py`).
Para cambiarla, vuelva a ejecutar el asistente.

## 6. Administrar la base de datos dentro de VS Code
1. Clic en el ícono **SQLTools** (cilindro) de la barra lateral.
2. Conexión **AquaWash (PostgreSQL)** > clic en *Connect now* > escriba la contraseña.
3. Despliegue *aquawash > public > Tables*: verá `clientes`, `vehiculos`, `servicios`, `citas`, `pagos`, `usuarios`.
   - Clic en el ícono de lupa de una tabla (*Show table records*) para ver sus datos.
   - Clic en el ícono de tabla para ver su estructura (columnas y claves).
4. Abra `sql/consultas.sql`, seleccione una consulta y pulse **Ctrl+E, Ctrl+E** para ejecutarla.
   También puede crear sus propios archivos `.sql` y ejecutarlos igual.

## 7. Ejecutar el programa
Pulse **F5** > **«AquaWash · 2) Aplicación de escritorio»** (o `python main.py`).

| Usuario  | Contraseña   | Rol      |
|----------|--------------|----------|
| admin    | admin123     | ADMIN    |
| operador | operador123  | OPERADOR |

**Página web:** menú *Archivo > Abrir página web* (http://localhost:8000).
O ejecute **«AquaWash · Solo servidor web»** desde F5.
Las reservas web aparecen en la pestaña *Agenda* con origen WEB, y también en SQLTools (consulta 5).

## 8. Estructura
```
aquawash/
├── main.py                  # Aplicación de escritorio
├── setup_db.py              # Crea BD, tablas y datos (--demo)
├── config.py                # Conexión y parámetros
├── requirements.txt
├── docker-compose.yml       # (opcional) PostgreSQL en Docker
├── aquawash.code-workspace
├── .vscode/                 # SQLTools, F5 y tareas ya configurados
├── sql/
│   ├── consultas.sql        # Consultas de administración
│   └── datos_demo.sql       # Datos de ejemplo
├── database/                # schema.sql + db.py (reglas de negocio)
├── ui/                      # Pantallas Tkinter
└── web/                     # server.py + index.html
```

## 9. Problemas frecuentes
- **«password authentication failed»**: la contraseña de `config.py` no coincide con la de PostgreSQL.
- **«connection refused»**: el servicio de PostgreSQL no está iniciado (o Docker apagado).
- **SQLTools pide instalar el driver**: acepte; instala *SQLTools PostgreSQL Driver*.
- **«No module named tkinter»** (Linux): `sudo apt install python3-tk`.
