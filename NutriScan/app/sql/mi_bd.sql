-- =============================================================
-- 1. FUNCIÓN DE ACTUALIZACIÓN AUTOMÁTICA (AUDITORÍA)
-- =============================================================
-- Esta función actualiza automáticamente el campo fecha_actualizacion en cada UPDATE
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- 2. CREACIÓN DE ESTRUCTURA (DDL)
-- =============================================================

-- TABLA ROLES
CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_roles BEFORE UPDATE ON roles FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA MODULOS
CREATE TABLE modulos (
    id_modulo SERIAL PRIMARY KEY,
    nombre_modulo VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_modulos BEFORE UPDATE ON modulos FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA USUARIOS
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    identificacion VARCHAR(20) NOT NULL UNIQUE, 
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    genero VARCHAR(15),
    pais VARCHAR(50),
    departamento VARCHAR(50),
    ciudad VARCHAR(50),
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_usuarios BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA TELEFONO
CREATE TABLE telefono (
    id_telefono SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    numero VARCHAR(20) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'Movil',
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_telefono BEFORE UPDATE ON telefono FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA PERFILES CLINICOS
CREATE TABLE perfiles_clinicos (
    id_perfil SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    edad INT,
    peso_kg DECIMAL(5,2),
    altura_cm DECIMAL(5,2),
    biotipo VARCHAR(20) DEFAULT 'No Definido',
    confianza_ia DECIMAL(5,4),
    meta_calorica_diaria INT,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_perfiles BEFORE UPDATE ON perfiles_clinicos FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA ALIMENTOS
CREATE TABLE alimentos (
    id_alimento SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50), 
    calorias INT NOT NULL,
    proteinas_g DECIMAL(5,2) DEFAULT 0,
    carbohidratos_g DECIMAL(5,2) DEFAULT 0,
    grasas_g DECIMAL(5,2) DEFAULT 0,
    fibra_g DECIMAL(5,2) DEFAULT 0,
    azucares_g DECIMAL(5,2) DEFAULT 0,
    sodio_mg DECIMAL(6,2) DEFAULT 0,
    vitaminas TEXT,
    minerales TEXT,
    es_apto_diabetico BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_alimentos BEFORE UPDATE ON alimentos FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA PERMISOS ROLES
CREATE TABLE permisos_roles (
    id_permiso SERIAL PRIMARY KEY,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    id_modulo INT NOT NULL REFERENCES modulos(id_modulo),
    puede_leer BOOLEAN DEFAULT TRUE,
    puede_escribir BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_permisos BEFORE UPDATE ON permisos_roles FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA REGISTRO CONSUMO
CREATE TABLE registro_consumo (
    id_registro SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    id_alimento INT NOT NULL REFERENCES alimentos(id_alimento),
    cantidad_gramos DECIMAL(6,2) NOT NULL,
    fecha_consumo DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_consumo BEFORE UPDATE ON registro_consumo FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA HISTORIAL SESION
CREATE TABLE historial (
    id_historial SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    fecha_inicio DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_historial BEFORE UPDATE ON historial FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA HISTORIAL CHAT IA
CREATE TABLE historial_chat (
    id_chat SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    id_historial INT REFERENCES historial(id_historial),
    pregunta_usuario TEXT NOT NULL,
    respuesta_ia TEXT NOT NULL,
    flag_revision_nutricionista BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_chat_ia BEFORE UPDATE ON historial_chat FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- =============================================================
-- 3. INSERCIÓN MASIVA DE DATOS (DML)
-- =============================================================

-- 3.1 ROLES (Solo los 3 requeridos)
INSERT INTO roles (nombre_rol) VALUES 
('Administrador'), ('Nutricionista'), ('Paciente');

-- 3.2 MODULOS
INSERT INTO modulos (nombre_modulo) VALUES 
('Dashboard'), ('Usuarios'), ('Alimentos'), ('Reportes'), ('Configuracion'),
('Pagos'), ('Citas'), ('Chat IA'), ('Historial Clinico'), ('Notificaciones');

-- 3.3 USUARIOS (10 registros ajustados a los 3 roles)
INSERT INTO usuarios (identificacion, nombre_completo, email, genero, pais, departamento, ciudad, password_hash, id_rol) VALUES
('1001', 'Juan Perez', 'juan.admin@app.com', 'Masculino', 'Colombia', 'Bogota', 'Bogota', 'hash_admin_1', 1),
('1002', 'Dra. Maria Lopez', 'maria.nutri@app.com', 'Femenino', 'Colombia', 'Antioquia', 'Medellin', 'hash_nutri_2', 2),
('1003', 'Carlos Cliente', 'carlos.paciente@gmail.com', 'Masculino', 'Mexico', 'CDMX', 'CDMX', 'hash_pac_3', 3),
('1004', 'Ana Garcia', 'ana.paciente@gmail.com', 'Femenino', 'Argentina', 'BA', 'Buenos Aires', 'hash_pac_4', 3),
('1005', 'Pedro Gomez', 'pedro.paciente@app.com', 'Masculino', 'Chile', 'Santiago', 'Santiago', 'hash_pac_5', 3),
('1006', 'Laura Martinez', 'laura.paciente@app.com', 'Femenino', 'Peru', 'Lima', 'Lima', 'hash_pac_6', 3),
('1007', 'Sofia Rojas', 'sofia.paciente@yahoo.com', 'Femenino', 'Colombia', 'Valle', 'Cali', 'hash_pac_7', 3),
('1008', 'Miguel Torres', 'miguel.paciente@hotmail.com', 'Masculino', 'Colombia', 'Valle', 'Cali', 'hash_pac_8', 3),
('1009', 'Lucia Mendez', 'lucia.paciente@outlook.com', 'Femenino', 'Colombia', 'Atlantico', 'Barranquilla', 'hash_pac_9', 3),
('1010', 'David Ramirez', 'david.paciente@app.com', 'Masculino', 'Colombia', 'Bogota', 'Bogota', 'hash_pac_10', 3);

-- 3.4 TELEFONOS
INSERT INTO telefono (id_usuario, numero, tipo) VALUES
(1, '3001110001', 'Movil'), (2, '3001110002', 'Consultorio'), (3, '3001110003', 'Movil'),
(4, '3001110004', 'Movil'), (5, '3001110005', 'Movil'), (6, '3001110006', 'Movil'),
(7, '3001110007', 'Movil'), (8, '3001110008', 'Movil'), (9, '3001110009', 'Movil'), (10, '3001110010', 'Movil');

-- 3.5 PERFILES CLINICOS
INSERT INTO perfiles_clinicos (id_usuario, edad, peso_kg, altura_cm, biotipo, meta_calorica_diaria) VALUES
(1, 35, 80.0, 175.0, 'Mesomorfo', 2500), (2, 29, 60.0, 165.0, 'Ectomorfo', 2000),
(3, 40, 95.5, 180.0, 'Endomorfo', 1800), (4, 25, 55.0, 160.0, 'Ectomorfo', 2200),
(5, 30, 85.0, 178.0, 'Mesomorfo', 3000), (6, 28, 62.0, 168.0, 'No Definido', 2000),
(7, 33, 70.0, 170.0, 'Endomorfo', 1900), (8, 45, 88.0, 172.0, 'Mesomorfo', 2400),
(9, 22, 50.0, 158.0, 'Ectomorfo', 2100), (10, 27, 75.0, 176.0, 'Mesomorfo', 2300);

-- 3.6 ALIMENTOS
INSERT INTO alimentos (nombre, categoria, calorias, proteinas_g, carbohidratos_g, grasas_g, es_apto_diabetico) VALUES
('Pechuga de Pollo', 'Proteina', 165, 31.0, 0.0, 3.6, TRUE), 
('Arroz Blanco', 'Carbohidrato', 130, 2.7, 28.0, 0.3, TRUE),
('Huevo Cocido', 'Proteina', 155, 13.0, 1.1, 11.0, TRUE), 
('Manzana', 'Fruta', 52, 0.3, 14.0, 0.2, TRUE),
('Avena', 'Cereal', 389, 16.9, 66.0, 6.9, TRUE), 
('Salmon', 'Pescado', 208, 20.0, 0.0, 13.0, TRUE),
('Aguacate', 'Grasa', 160, 2.0, 9.0, 15.0, TRUE), 
('Leche Entera', 'Lacteo', 42, 3.4, 5.0, 1.0, TRUE),
('Pan Integral', 'Cereal', 265, 9.0, 49.0, 3.0, TRUE), 
('Almendras', 'Fruto Seco', 579, 21.0, 22.0, 50.0, TRUE);

-- 3.7 PERMISOS ROLES
INSERT INTO permisos_roles (id_rol, id_modulo, puede_leer, puede_escribir, puede_editar) VALUES
(1, 1, TRUE, TRUE, TRUE), (1, 2, TRUE, TRUE, TRUE), (1, 3, TRUE, TRUE, TRUE),
(2, 3, TRUE, TRUE, TRUE), (2, 9, TRUE, TRUE, TRUE), (2, 8, TRUE, TRUE, FALSE),
(3, 1, TRUE, FALSE, FALSE), (3, 8, TRUE, TRUE, FALSE), (3, 4, TRUE, FALSE, FALSE), (3, 9, TRUE, FALSE, FALSE);

-- 3.8 REGISTRO CONSUMO
INSERT INTO registro_consumo (id_usuario, id_alimento, cantidad_gramos) VALUES
(3, 1, 200.0), (3, 2, 150.0), (4, 4, 100.0), (4, 5, 50.0), (7, 3, 2.0),
(8, 6, 180.0), (9, 7, 50.0), (3, 10, 30.0), (4, 8, 200.0), (10, 9, 60.0);

-- 3.9 HISTORIAL SESION
INSERT INTO historial (id_usuario) VALUES
(3), (4), (5), (6), (7), (8), (9), (10);

-- 3.10 HISTORIAL CHAT IA
INSERT INTO historial_chat (id_usuario, id_historial, pregunta_usuario, respuesta_ia) VALUES
(3, 1, '¿Cuántas calorías tiene el pollo?', 'El pollo tiene aprox 165 cal por 100g.'),
(3, 1, 'Quiero bajar de peso', 'Debes mantener un déficit calórico.'),
(4, 2, '¿Puedo comer pan si soy celiaca?', 'No, el pan común tiene gluten.'),
(5, 3, 'Rutina para bajar de peso', 'Enfócate en déficit calórico y ejercicio de fuerza.'),
(10, 8, '¿Qué es la creatina?', 'Es un suplemento para mejorar el rendimiento físico.');
