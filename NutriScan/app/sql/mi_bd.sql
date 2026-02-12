-- =============================================================
-- 2. CREACIÓN DE ESTRUCTURA (DDL)
-- =============================================================

CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE modulos (
    id_modulo SERIAL PRIMARY KEY,
    nombre_modulo VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE, 
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    genero VARCHAR(15),
    pais VARCHAR(50),
    departamento VARCHAR(50),
    ciudad VARCHAR(50),
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telefono (
    id_telefono SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    numero VARCHAR(20) NOT NULL,
    tipo VARCHAR(20) DEFAULT 'Movil',
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE perfiles_clinicos (
    id_perfil SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    edad INT,
    peso_kg DECIMAL(5,2),
    altura_cm DECIMAL(5,2),
    biotipo VARCHAR(20) DEFAULT 'No Definido',
    confianza_ia DECIMAL(5,4),
    meta_calorica_diaria INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alimentos (
    id_alimento SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50), 
    calorias INT NOT NULL,
    proteinas_g DECIMAL(5,2) DEFAULT 0,
    carbohidratos_g DECIMAL(5,2) DEFAULT 0,
    grasas_g DECIMAL(5,2) DEFAULT 0,
    es_apto_diabetico BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo'
);

CREATE TABLE permisos_roles (
    id_permiso SERIAL PRIMARY KEY,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    id_modulo INT NOT NULL REFERENCES modulos(id_modulo),
    puede_leer BOOLEAN DEFAULT TRUE,
    puede_escribir BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE
);

CREATE TABLE registro_consumo (
    id_registro SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    id_alimento INT NOT NULL REFERENCES alimentos(id_alimento),
    cantidad_gramos DECIMAL(6,2) NOT NULL,
    fecha_consumo DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE historial_chat (
    id_chat SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    pregunta_usuario TEXT,
    respuesta_ia TEXT,
    flag_revision_nutricionista BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================
-- 3. INSERCIÓN MASIVA DE DATOS (DML - 10 REGISTROS POR TABLA)
-- =============================================================

-- 3.1 ROLES (10)
INSERT INTO roles (nombre_rol) VALUES 
('Administrador'), ('Nutricionista'), ('Paciente'), ('Entrenador'), ('Soporte'),
('Auditor'), ('Gerente'), ('Desarrollador'), ('Invitado'), ('Practicante');

-- 3.2 MODULOS (10)
INSERT INTO modulos (nombre_modulo) VALUES 
('Dashboard'), ('Usuarios'), ('Alimentos'), ('Reportes'), ('Configuracion'),
('Pagos'), ('Citas'), ('Chat IA'), ('Historial Clinico'), ('Notificaciones');

-- 3.3 USUARIOS (10 Personas variadas)
-- Asumimos IDs del 1 al 10 basados en el orden de inserción de roles
INSERT INTO usuarios (cedula, nombre_completo, email, genero, pais, departamento, ciudad, password_hash, id_rol) VALUES
('1001', 'Juan Perez', 'juan.admin@app.com', 'Masculino', 'Colombia', 'Bogota', 'Bogota', 'pass1', 1), -- Admin
('1002', 'Dra. Maria Lopez', 'maria.nutri@app.com', 'Femenino', 'Colombia', 'Antioquia', 'Medellin', 'pass2', 2), -- Nutri
('1003', 'Carlos Cliente', 'carlos.c@gmail.com', 'Masculino', 'Mexico', 'CDMX', 'CDMX', 'pass3', 3), -- Paciente
('1004', 'Ana Paciente', 'ana.p@gmail.com', 'Femenino', 'Argentina', 'BA', 'Buenos Aires', 'pass4', 3), -- Paciente
('1005', 'Pedro Fitness', 'pedro.fit@gym.com', 'Masculino', 'Chile', 'Santiago', 'Santiago', 'pass5', 4), -- Entrenador
('1006', 'Laura Soporte', 'laura.help@app.com', 'Femenino', 'Peru', 'Lima', 'Lima', 'pass6', 5), -- Soporte
('1007', 'Sofia Garcia', 'sofia.g@yahoo.com', 'Femenino', 'Espana', 'Madrid', 'Madrid', 'pass7', 3), -- Paciente
('1008', 'Miguel Torres', 'miguel.t@hotmail.com', 'Masculino', 'Colombia', 'Valle', 'Cali', 'pass8', 3), -- Paciente
('1009', 'Lucia Mendez', 'lucia.m@outlook.com', 'Femenino', 'Colombia', 'Atlantico', 'Barranquilla', 'pass9', 3), -- Paciente
('1010', 'David Developer', 'david.dev@app.com', 'Masculino', 'Uruguay', 'Montevideo', 'Montevideo', 'pass10', 8); -- Dev

-- 3.4 TELEFONOS (10 - Uno para cada usuario creado arriba)
INSERT INTO telefono (id_usuario, numero, tipo) VALUES
(1, '3001110001', 'Movil'),
(2, '3001110002', 'Consultorio'),
(3, '3001110003', 'Movil'),
(4, '3001110004', 'Casa'),
(5, '3001110005', 'Trabajo'),
(6, '3001110006', 'Movil'),
(7, '3001110007', 'Movil'),
(8, '3001110008', 'Movil'),
(9, '3001110009', 'Casa'),
(10, '3001110010', 'Oficina');

-- 3.5 PERFILES CLINICOS (10 - Uno para cada usuario)
INSERT INTO perfiles_clinicos (id_usuario, edad, peso_kg, altura_cm, biotipo, meta_calorica_diaria) VALUES
(1, 35, 80.0, 175.0, 'Mesomorfo', 2500),
(2, 29, 60.0, 165.0, 'Ectomorfo', 2000),
(3, 40, 95.5, 180.0, 'Endomorfo', 1800),
(4, 25, 55.0, 160.0, 'Ectomorfo', 2200),
(5, 30, 85.0, 178.0, 'Mesomorfo', 3000),
(6, 28, 62.0, 168.0, 'No Definido', 2000),
(7, 33, 70.0, 170.0, 'Endomorfo', 1900),
(8, 45, 88.0, 172.0, 'Mesomorfo', 2400),
(9, 22, 50.0, 158.0, 'Ectomorfo', 2100),
(10, 27, 75.0, 176.0, 'Mesomorfo', 2300);

-- 3.6 ALIMENTOS (10)
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

-- 3.7 PERMISOS ROLES (10 Relaciones)
INSERT INTO permisos_roles (id_rol, id_modulo, puede_leer, puede_escribir) VALUES
(1, 1, TRUE, TRUE), -- Admin ve Dashboard
(1, 2, TRUE, TRUE), -- Admin edita Usuarios
(1, 6, TRUE, TRUE), -- Admin ve Pagos
(2, 3, TRUE, TRUE), -- Nutri edita Alimentos
(2, 9, TRUE, TRUE), -- Nutri ve Historial Clinico
(3, 1, TRUE, FALSE), -- Paciente ve Dashboard
(3, 8, TRUE, TRUE), -- Paciente usa Chat
(3, 4, TRUE, FALSE), -- Paciente ve Reportes
(4, 9, TRUE, FALSE), -- Entrenador ve Historial
(5, 5, TRUE, TRUE); -- Soporte configura Sistema

-- 3.8 REGISTRO CONSUMO (10 Registros de comida)
INSERT INTO registro_consumo (id_usuario, id_alimento, cantidad_gramos) VALUES
(3, 1, 200.0), -- Carlos comió Pollo
(3, 2, 150.0), -- Carlos comió Arroz
(4, 4, 100.0), -- Ana comió Manzana
(4, 5, 50.0),  -- Ana comió Avena
(7, 3, 2.0),   -- Sofia comió 2 Huevos (aprox gramaje implicito o unidad)
(8, 6, 180.0), -- Miguel comió Salmón
(9, 7, 50.0),  -- Lucia comió Aguacate
(3, 10, 30.0), -- Carlos comió Almendras
(4, 8, 200.0), -- Ana tomó Leche
(10, 9, 60.0); -- David comió Pan

-- 3.9 HISTORIAL CHAT (10 Conversaciones)
INSERT INTO historial_chat (id_usuario, pregunta_usuario, respuesta_ia) VALUES
(3, '¿Cuántas calorías tiene el pollo?', 'El pollo tiene aprox 165 cal por 100g.'),
(3, 'Quiero bajar de peso', 'Debes mantener un déficit calórico.'),
(4, '¿Puedo comer pan si soy celiaca?', 'No, el pan común tiene gluten.'),
(4, 'Receta de desayuno', 'Prueba avena con manzana.'),
(7, '¿Qué es mejor cardio o pesas?', 'Una combinación de ambos es ideal.'),
(8, '¿El aguacate engorda?', 'Es grasa saludable, pero consúmelo con moderación.'),
(9, 'Tengo ansiedad por dulce', 'Prueba comer fruta o chocolate negro.'),
(3, 'Rutina para pecho', 'Press de banca y flexiones.'),
(4, '¿Cuánta agua debo tomar?', 'Aproximadamente 2 litros al día.'),
(10, '¿La creatina es segura?', 'Sí, es uno de los suplementos más estudiados.');