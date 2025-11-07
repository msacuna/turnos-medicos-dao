-- Creación de los esquemas según el DER (formato MySQL)

-- =============================================================================
-- Usuarios (roles y usuarios)
-- =============================================================================
CREATE TABLE rol (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE usuario (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    id_rol INT NOT NULL,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES rol(id)
);

-- =============================================================================
-- Laboratorios (medicamentos y laboratorios)
-- =============================================================================
CREATE TABLE laboratorio (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE medicamento (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE medicamento_laboratorio (
    id_medicamento INT NOT NULL,
    id_laboratorio INT NOT NULL,
    CONSTRAINT pk_medicamento_laboratorio PRIMARY KEY (id_medicamento, id_laboratorio),
    CONSTRAINT fk_medicamento_laboratorio_medicamento FOREIGN KEY (id_medicamento) REFERENCES medicamento(id) ON DELETE CASCADE,
    CONSTRAINT fk_medicamento_laboratorio_laboratorio FOREIGN KEY (id_laboratorio) REFERENCES laboratorio(id) ON DELETE CASCADE
);

-- Obras sociales
CREATE TABLE tipo_obra_social (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE obra_social (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    cuit VARCHAR(11) NOT NULL,
    porcentaje_cobertura DECIMAL(5, 2) NOT NULL,
    id_tipo INT NOT NULL,
    CONSTRAINT chk_porcentaje CHECK (porcentaje_cobertura >= 0 AND porcentaje_cobertura <= 100),
    CONSTRAINT fk_obra_social_tipo FOREIGN KEY (id_tipo) REFERENCES tipo_obra_social(id)
);

-- =============================================================================
-- Pacientes (paciente, grupo sanguineo, alergias, antecedentes)
-- =============================================================================
CREATE TABLE grupo_sanguineo (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(5) NOT NULL UNIQUE -- 'A+', 'O-'
);

CREATE TABLE alergia (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE antecedente (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE paciente (
    dni INT NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    id_grupo_sanguineo INT NOT NULL,
    id_obra_social INT,
    CONSTRAINT fk_paciente_grupo_sanguineo FOREIGN KEY (id_grupo_sanguineo) REFERENCES grupo_sanguineo(id),
    CONSTRAINT fk_paciente_obra_social FOREIGN KEY (id_obra_social) REFERENCES obra_social(id) ON DELETE SET NULL
);

CREATE TABLE paciente_alergia (
    dni_paciente INT NOT NULL,
    id_alergia INT NOT NULL,
    CONSTRAINT pk_paciente_alergia PRIMARY KEY (dni_paciente, id_alergia),
    CONSTRAINT fk_paciente_alergia_paciente FOREIGN KEY (dni_paciente) REFERENCES paciente(dni) ON DELETE CASCADE,
    CONSTRAINT fk_paciente_alergia_alergia FOREIGN KEY (id_alergia) REFERENCES alergia(id) ON DELETE CASCADE
);

CREATE TABLE paciente_antecedente (
    dni_paciente INT NOT NULL,
    id_antecedente INT NOT NULL,
    CONSTRAINT pk_paciente_antecedente PRIMARY KEY (dni_paciente, id_antecedente),
    CONSTRAINT fk_paciente_antecedente_paciente FOREIGN KEY (dni_paciente) REFERENCES paciente(dni) ON DELETE CASCADE,
    CONSTRAINT fk_paciente_antecedente_antecedente FOREIGN KEY (id_antecedente) REFERENCES antecedente(id) ON DELETE CASCADE
);

-- =============================================================================
-- Profesionales (profesional, horarios atencion, especialidad, agenda)
-- =============================================================================
CREATE TABLE especialidad (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE horario_atencion (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    CONSTRAINT chk_hora CHECK (hora_fin > hora_inicio)
);

CREATE TABLE profesional (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL,
    id_especialidad INT NOT NULL,
    CONSTRAINT fk_profesional_especialidad FOREIGN KEY (id_especialidad) REFERENCES especialidad(id)
);

-- si CURDATE() <= '15' → permitir UPDATE o INSERT en horario_profesional
CREATE TABLE horario_profesional (
    id_profesional INT NOT NULL,
    id_horario_atencion INT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_horario_profesional PRIMARY KEY (id_profesional, id_horario_atencion),
    CONSTRAINT fk_horario_profesional_profesional FOREIGN KEY (id_profesional) REFERENCES profesional(id) ON DELETE CASCADE,
    CONSTRAINT fk_horario_profesional_horario FOREIGN KEY (id_horario_atencion) REFERENCES horario_atencion(id) ON DELETE CASCADE
);

CREATE TABLE obra_social_profesional (
    id_obra_social INT NOT NULL,
    id_profesional INT NOT NULL,
    vigente BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_obra_social_profesional PRIMARY KEY (id_obra_social, id_profesional),
    CONSTRAINT fk_obra_social_profesional_obra_social FOREIGN KEY (id_obra_social) REFERENCES obra_social(id) ON DELETE CASCADE,
    CONSTRAINT fk_obra_social_profesional_profesional FOREIGN KEY (id_profesional) REFERENCES profesional(id) ON DELETE CASCADE
);

CREATE TABLE agenda_profesional (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_profesional INT NOT NULL,
    anio INT NOT NULL,
    mes INT NOT NULL,
    CONSTRAINT chk_mes CHECK (mes >= 1 AND mes <= 12),
    CONSTRAINT fk_agenda_profesional_profesional FOREIGN KEY (id_profesional) REFERENCES profesional(id)
);

-- =============================================================================
-- Turnos (turno, estado turno, receta, consulta, motivo consulta)
-- =============================================================================
CREATE TABLE estado_turno (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE turno (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin_estimada TIME NOT NULL,
    dni_paciente INT NOT NULL,
    id_estado INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_agenda_profesional INT NOT NULL,
    CONSTRAINT chk_hora_turno CHECK (hora_fin_estimada > hora_inicio),
    CONSTRAINT fk_turno_especialidad FOREIGN KEY (id_especialidad) REFERENCES especialidad(id),
    CONSTRAINT fk_turno_agenda_profesional FOREIGN KEY (id_agenda_profesional) REFERENCES agenda_profesional(id),
    CONSTRAINT fk_turno_paciente FOREIGN KEY (dni_paciente) REFERENCES paciente(dni),
    CONSTRAINT fk_turno_estado FOREIGN KEY (id_estado) REFERENCES estado_turno(id)
);

CREATE TABLE receta (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    dispensada BOOLEAN NOT NULL DEFAULT FALSE -- farmacia entregó medicamentos
);

CREATE TABLE detalle_receta (
    item INT NOT NULL AUTO_INCREMENT,
    id_receta INT NOT NULL,
    id_medicamento INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    indicaciones VARCHAR(255),
    CONSTRAINT pk_detalle_receta PRIMARY KEY (item, id_receta),
    CONSTRAINT fk_detalle_receta_receta FOREIGN KEY (id_receta) REFERENCES receta(id) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_receta_medicamento FOREIGN KEY (id_medicamento) REFERENCES medicamento(id)
);

CREATE TABLE motivo_consulta (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE -- general, control, urgencia
);

CREATE TABLE consulta (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    observaciones VARCHAR(255), -- notas del profesional
    id_turno INT NOT NULL,
    id_motivo_consulta INT NOT NULL,
    id_receta INT,
    CONSTRAINT fk_consulta_turno FOREIGN KEY (id_turno) REFERENCES turno(id) ON DELETE CASCADE,
    CONSTRAINT fk_consulta_motivo_consulta FOREIGN KEY (id_motivo_consulta) REFERENCES motivo_consulta(id),
    CONSTRAINT fk_consulta_receta FOREIGN KEY (id_receta) REFERENCES receta(id) ON DELETE SET NULL
);

CREATE INDEX idx_turno_paciente ON turno(dni_paciente);
CREATE INDEX idx_consulta_turno ON consulta(id_turno);
CREATE INDEX idx_paciente_alergia_paciente ON paciente_alergia(dni_paciente);
CREATE INDEX idx_paciente_antecedente_paciente ON paciente_antecedente(dni_paciente);