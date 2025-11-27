-- Inicialización de datos (inserts)
INSERT INTO rol (nombre) VALUES
('Administrador'), ('Profesional');

INSERT INTO grupo_sanguineo (nombre) VALUES
('A+'), ('A-'),
('B+'), ('B-'),
('AB+'), ('AB-'),
('0+'), ('0-');

INSERT INTO estados_turno (nombre) VALUES
('Disponible'), -- turno sin paciente asignado
('Cancelado'), -- se cancelo el turno
('En proceso'), -- llegó a fecha_hora_inicio y se agenda como atendido 15 min antes de fecha_hora_fin
('Ausente'), -- llegó a fecha_hora_inicio y no fue atendido
('Finalizado'), -- finalizo el turno y fue atendido
('Agendado'); -- se asocio un paciente al turno

INSERT INTO especialidad (nombre, precio) VALUES
('Cardiologia', 1500.00),
('Dermatologia', 1325.00),
('Endocrinologia', 1420.00),
('Gastroenterologia', 1180.00),
('Neurologia', 2050.00),
('Pediatria', 950.00),
('Psiquiatria', 1105.00),
('Traumatologia', 1600.00),
('Urologia', 1250.00);
INSERT INTO especialidad (nombre, precio) VALUES
('Chequeo General', 800.00),
('Seguimiento de tratamiento', 950.50),
('Control', 700.25),
('Dolor', 1200.75),
('Urgencia', 1600.00);

INSERT INTO alergia (nombre) VALUES
('Penicilina'),
('Ibuprofeno'),
('Polvo'),
('Polenes'),
('Picaduras de insectos'),
('Lacteos');

INSERT INTO antecedente (nombre) VALUES
('Diabetes'),
('Hipertension'),
('Asma'),
('Enfermedad cardiaca'),
('Colesterol alto'),
('Tabaquismo'),
('Obesidad');

INSERT INTO motivo_consulta (nombre) VALUES
('Consulta General'),
('Control'),
('Urgencia'),
('Seguimiento');

INSERT INTO tipo_obra_social (nombre) VALUES
('Nacional'),
('Provincial'),
('Jubilado');

INSERT INTO obra_social (nombre, cuit, porcentaje_cobertura, nombre_tipo) VALUES
('OSDE', '30573419671', 90.00, 'Nacional'),
('Swiss Medical', '30678945211', 85.00, 'Nacional'),
('APROSS', '30500612781', 90.00, 'Nacional'),
('Galeno', '30710002911', 80.00, 'Provincial'),
('OSECAC', '30517890123', 80.00, 'Provincial'),
('PAMI', '30523467891', 100.00, 'Jubilado');

-- =============================================================================
-- Profesionales de ejemplo para testing
-- =============================================================================
INSERT INTO profesional (matricula, nombre, apellido, email, telefono, id_especialidad) VALUES
('MP001', 'Ana', 'Rodriguez', 'ana.rodriguez@hospital.com', '351-1234567', 1), -- Cardiologia  
('MP002', 'Carlos', 'Martinez', 'carlos.martinez@hospital.com', '351-2345678', 2), -- Dermatologia
('MP003', 'Maria', 'Lopez', 'maria.lopez@hospital.com', '351-3456789', 6), -- Pediatria
('MP004', 'Juan', 'Garcia', 'juan.garcia@hospital.com', '351-4567890', 8), -- Traumatologia
('MP005', 'Laura', 'Fernandez', 'laura.fernandez@hospital.com', '351-5678901', 3); -- Endocrinologia

-- =============================================================================
-- Relaciones profesional-obra social (algunos ejemplos)
-- =============================================================================
INSERT INTO obra_social_profesional (nombre_obra_social, id_profesional, vigente) VALUES
('OSDE', 1, TRUE),
('Swiss Medical', 1, TRUE),
('APROSS', 2, TRUE),
('Galeno', 2, TRUE),
('OSDE', 3, TRUE),
('PAMI', 3, TRUE),
('Swiss Medical', 4, TRUE),
('APROSS', 5, TRUE);

-- =============================================================================
-- Pacientes de ejemplo para testing
-- =============================================================================
INSERT INTO paciente (dni, nombre, apellido, fecha_nacimiento, email, telefono, nombre_grupo_sanguineo, nombre_obra_social) VALUES
(11111111, 'Juan', 'Perez', '1985-03-15', 'juan.perez.script@email.com', '351-1111111', 'A+', 'OSDE'),
(23456789, 'Maria', 'Gonzalez', '1990-07-22', 'maria.gonzalez@email.com', '351-2222222', 'B+', 'Swiss Medical'),
(34567890, 'Carlos', 'Rodriguez', '1978-11-08', 'carlos.rodriguez@email.com', '351-3333333', '0+', 'APROSS'),
(45678901, 'Ana', 'Martinez', '1995-01-30', 'ana.martinez@email.com', '351-4444444', 'AB+', 'Galeno'),
(56789012, 'Luis', 'Lopez', '1982-09-12', 'luis.lopez@email.com', '351-5555555', 'A-', 'OSECAC'),
(67890123, 'Laura', 'Silva', '1988-04-18', 'laura.silva@email.com', '351-6666666', 'B-', 'PAMI'),
(78901234, 'Pedro', 'Morales', '1975-12-03', 'pedro.morales@email.com', '351-7777777', '0-', 'OSDE'),
(89012345, 'Sofia', 'Gutierrez', '1992-06-25', 'sofia.gutierrez@email.com', '351-8888888', 'AB-', 'Swiss Medical');

-- =============================================================================
-- Ejemplo de turno
-- =============================================================================
INSERT INTO turno (fecha, hora_inicio, hora_fin_estimada, dni_paciente, nombre_estado, id_especialidad, id_agenda_profesional, monto) VALUES
('2025-12-15', '09:00:00', '09:30:00', 11111111, 'Agendado', 1, 1, 1500.00);



