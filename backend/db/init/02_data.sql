-- Inicialización de datos (inserts)
INSERT INTO rol (nombre) VALUES
('Administrador'), ('Profesional');

INSERT INTO grupo_sanguineo (nombre) VALUES
('A+'), ('A-'),
('B+'), ('B-'),
('AB+'), ('AB-'),
('O+'), ('O-');

INSERT INTO estado_turno (nombre) VALUES
('Agendado'), -- no llegó a fecha_hora_inicio
('Cancelado'), -- cancelado antes de fecha_hora_inicio
('En proceso'), -- llegó a fecha_hora_inicio y se agenda como atendido 15 min antes de fecha_hora_fin
('Ausente'), -- llegó a fecha_hora_inicio y no se agenda como atendido 15 min antes de fecha_hora_fin
('Finalizado'), -- llegó a fecha_hora_inicio y fue atendido
('Confirmado'); -- se acepta la generación de consulta asociada al turno

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