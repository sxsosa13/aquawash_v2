-- AquaWash · Consultas de administración
-- En VS Code (SQLTools): conéctese a «AquaWash (PostgreSQL)», seleccione una consulta
-- y pulse Ctrl+E y luego Ctrl+E (o clic derecho > Run selected query).

-- 1) Citas de hoy
SELECT c.id, c.hora, cl.nombre AS cliente, v.placa, s.nombre AS servicio, c.estado, c.origen
FROM citas c
JOIN vehiculos v ON v.id = c.vehiculo_id
JOIN clientes cl ON cl.id = v.cliente_id
JOIN servicios s ON s.id = c.servicio_id
WHERE c.fecha = CURRENT_DATE
ORDER BY c.hora;

-- 2) Ingresos por día (últimos 30 días)
SELECT fecha::date AS dia, SUM(monto) AS total, COUNT(*) AS cobros
FROM pagos
WHERE fecha >= CURRENT_DATE - 30
GROUP BY 1 ORDER BY 1 DESC;

-- 3) Servicios más solicitados
SELECT s.nombre, COUNT(*) AS veces
FROM citas c JOIN servicios s ON s.id = c.servicio_id
WHERE c.estado <> 'CANCELADA'
GROUP BY s.nombre ORDER BY veces DESC;

-- 4) Vehículos por cliente
SELECT cl.nombre, v.tipo, v.placa, v.marca, v.modelo
FROM clientes cl JOIN vehiculos v ON v.cliente_id = cl.id
ORDER BY cl.nombre, v.placa;

-- 5) Reservas hechas desde la web
SELECT c.id, c.fecha, c.hora, v.placa, c.estado
FROM citas c JOIN vehiculos v ON v.id = c.vehiculo_id
WHERE c.origen = 'WEB' ORDER BY c.fecha DESC, c.hora;

-- 6) Ocupación por horario (puestos usados)
SELECT fecha, hora, COUNT(*) AS puestos_usados
FROM citas WHERE estado <> 'CANCELADA' AND fecha >= CURRENT_DATE
GROUP BY fecha, hora ORDER BY fecha, hora;

-- 7) Conteo de registros por tabla
SELECT 'clientes' AS tabla, COUNT(*) FROM clientes
UNION ALL SELECT 'vehiculos', COUNT(*) FROM vehiculos
UNION ALL SELECT 'servicios', COUNT(*) FROM servicios
UNION ALL SELECT 'citas', COUNT(*) FROM citas
UNION ALL SELECT 'pagos', COUNT(*) FROM pagos;

-- 8) Estructura de columnas de todas las tablas
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' ORDER BY table_name, ordinal_position;
