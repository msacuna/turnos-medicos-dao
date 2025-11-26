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

INSERT INTO especialidad (nombre) VALUES
('Cardiologia'),
('Dermatologia'),
('Endocrinologia'),
('Gastroenterologia'),
('Neurologia'),
('Pediatria'),
('Psiquiatria'),
('Traumatologia'),
('Urologia');

INSERT INTO motivo_consulta (nombre) VALUES
('Chequeo General'),
('Seguimiento de tratamiento'),
('Control'),
('Dolor'),
('Urgencia');

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