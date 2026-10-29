-- Sosa Car Wash · Esquema PostgreSQL
-- Ejecutar en pgAdmin: clic derecho en la base "aquawash" > Query Tool > pegar > F5

CREATE TABLE IF NOT EXISTS usuarios (
    id      SERIAL PRIMARY KEY,
    usuario VARCHAR(30)  UNIQUE NOT NULL,
    clave   VARCHAR(200) NOT NULL,
    nombre  VARCHAR(80)  NOT NULL,
    rol     VARCHAR(10)  NOT NULL DEFAULT 'OPERADOR' CHECK (rol IN ('ADMIN','OPERADOR'))
);

CREATE TABLE IF NOT EXISTS clientes (
    id       SERIAL PRIMARY KEY,
    nombre   VARCHAR(80) NOT NULL,
    telefono VARCHAR(25) NOT NULL,
    email    VARCHAR(100),
    creado   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id         SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    tipo       VARCHAR(5) NOT NULL CHECK (tipo IN ('AUTO','MOTO')),
    placa      VARCHAR(12) UNIQUE NOT NULL,
    marca      VARCHAR(40),
    modelo     VARCHAR(40),
    color      VARCHAR(25)
);

CREATE TABLE IF NOT EXISTS servicios (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(60) NOT NULL,
    tipo_vehiculo VARCHAR(5)  NOT NULL CHECK (tipo_vehiculo IN ('AUTO','MOTO')),
    precio        NUMERIC(12,2) NOT NULL CHECK (precio >= 0),
    duracion_min  INT NOT NULL DEFAULT 60 CHECK (duracion_min > 0),
    activo        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS citas (
    id          SERIAL PRIMARY KEY,
    vehiculo_id INT  NOT NULL REFERENCES vehiculos(id),
    servicio_id INT  NOT NULL REFERENCES servicios(id),
    fecha       DATE NOT NULL,
    hora        TIME NOT NULL,
    estado      VARCHAR(12) NOT NULL DEFAULT 'PENDIENTE'
                CHECK (estado IN ('PENDIENTE','EN_PROCESO','COMPLETADA','CANCELADA')),
    origen      VARCHAR(10) NOT NULL DEFAULT 'ESCRITORIO' CHECK (origen IN ('ESCRITORIO','WEB')),
    observacion TEXT,
    creado      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pagos (
    id      SERIAL PRIMARY KEY,
    cita_id INT UNIQUE NOT NULL REFERENCES citas(id),
    monto   NUMERIC(12,2) NOT NULL,
    metodo  VARCHAR(15) NOT NULL CHECK (metodo IN ('EFECTIVO','TARJETA','TRANSFERENCIA')),
    fecha   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS insumos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(40) DEFAULT 'GENERAL',
    cantidad NUMERIC(12,2) NOT NULL DEFAULT 0,
    unidad VARCHAR(20) NOT NULL DEFAULT 'unidad',
    costo_unitario NUMERIC(12,2) NOT NULL DEFAULT 0,
    stock_minimo NUMERIC(12,2) NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    actualizado TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingresos (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    detalle VARCHAR(200) NOT NULL,
    monto NUMERIC(12,2) NOT NULL CHECK (monto >= 0),
    categoria VARCHAR(40) DEFAULT 'SERVICIO',
    creado TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS egresos (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    detalle VARCHAR(200) NOT NULL,
    monto NUMERIC(12,2) NOT NULL CHECK (monto >= 0),
    categoria VARCHAR(40) DEFAULT 'OPERATIVO',
    creado TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS contacto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    telefono VARCHAR(30),
    email VARCHAR(100),
    mensaje TEXT,
    creado TIMESTAMP DEFAULT NOW()
);
