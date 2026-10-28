-- Datos de ejemplo para pruebas y sustentación (se pueden ejecutar con: python setup_db.py --demo)
INSERT INTO clientes (nombre, telefono, email) VALUES
 ('María Gómez',   '555-0101', 'maria@correo.com'),
 ('Carlos Benítez','555-0102', NULL),
 ('Lucía Duarte',  '555-0103', 'lucia@correo.com'),
 ('Jorge Ramírez', '555-0104', NULL);

INSERT INTO vehiculos (cliente_id, tipo, placa, marca, modelo, color) VALUES
 ((SELECT id FROM clientes WHERE nombre = 'María Gómez'),    'AUTO', 'ABC123', 'Toyota', 'Corolla', 'Blanco'),
 ((SELECT id FROM clientes WHERE nombre = 'Carlos Benítez'), 'AUTO', 'DEF456', 'Honda',  'Civic',   'Gris'),
 ((SELECT id FROM clientes WHERE nombre = 'Carlos Benítez'), 'MOTO', 'MOT789', 'Yamaha', 'FZ 150',  'Negro'),
 ((SELECT id FROM clientes WHERE nombre = 'Lucía Duarte'),   'MOTO', 'MOT321', 'Honda',  'CB 125',  'Rojo'),
 ((SELECT id FROM clientes WHERE nombre = 'Jorge Ramírez'),  'AUTO', 'GHI654', 'Kia',    'Rio',     'Azul');

INSERT INTO citas (vehiculo_id, servicio_id, fecha, hora, estado, origen) VALUES
 ((SELECT id FROM vehiculos WHERE placa = 'ABC123'), (SELECT id FROM servicios WHERE nombre = 'Lavado completo'),       CURRENT_DATE - 3, '09:00', 'COMPLETADA', 'ESCRITORIO'),
 ((SELECT id FROM vehiculos WHERE placa = 'MOT789'), (SELECT id FROM servicios WHERE nombre = 'Lavado de moto'),        CURRENT_DATE - 3, '10:00', 'COMPLETADA', 'WEB'),
 ((SELECT id FROM vehiculos WHERE placa = 'DEF456'), (SELECT id FROM servicios WHERE nombre = 'Lavado + encerado'),     CURRENT_DATE - 2, '11:00', 'COMPLETADA', 'ESCRITORIO'),
 ((SELECT id FROM vehiculos WHERE placa = 'GHI654'), (SELECT id FROM servicios WHERE nombre = 'Lavado básico'),         CURRENT_DATE - 1, '15:00', 'COMPLETADA', 'WEB'),
 ((SELECT id FROM vehiculos WHERE placa = 'MOT321'), (SELECT id FROM servicios WHERE nombre = 'Lavado de moto'),        CURRENT_DATE - 1, '16:00', 'CANCELADA',  'WEB'),
 ((SELECT id FROM vehiculos WHERE placa = 'ABC123'), (SELECT id FROM servicios WHERE nombre = 'Lavado básico'),         CURRENT_DATE,     '14:00', 'PENDIENTE',  'ESCRITORIO'),
 ((SELECT id FROM vehiculos WHERE placa = 'MOT321'), (SELECT id FROM servicios WHERE nombre = 'Lavado + lubricación de cadena'), CURRENT_DATE, '15:00', 'PENDIENTE', 'WEB'),
 ((SELECT id FROM vehiculos WHERE placa = 'DEF456'), (SELECT id FROM servicios WHERE nombre = 'Lavado completo'),       CURRENT_DATE + 1, '09:00', 'PENDIENTE',  'WEB');

INSERT INTO pagos (cita_id, monto, metodo, fecha)
SELECT c.id, s.precio, (ARRAY['EFECTIVO','TARJETA','TRANSFERENCIA'])[1 + c.id % 3], c.fecha + c.hora
FROM citas c JOIN servicios s ON s.id = c.servicio_id
WHERE c.estado = 'COMPLETADA';
