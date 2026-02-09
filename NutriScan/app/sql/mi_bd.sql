-- =============================================================
-- SCRIPT COMPLETO: BASE DE DATOS NUTRISCAN PRO (CON UBICACIONES)
-- =============================================================

-- 2. CREACIÓN DE ESTRUCTURA (DDL)

CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modulos (
    id_modulo SERIAL PRIMARY KEY,
    nombre_modulo VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    cedula VARCHAR(20) NOT NULL UNIQUE, 
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    genero VARCHAR(15),
    -- CAMPOS DE UBICACIÓN vienen del servicio externo
    pais VARCHAR(50),
    departamento VARCHAR(50),
    ciudad VARCHAR(50),
    ---------------------------------------------------------
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perfiles_clinicos (
    id_perfil SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    edad INT,
    peso_kg DECIMAL(5,2),
    altura_cm DECIMAL(5,2),
    biotipo VARCHAR(20) DEFAULT 'No Definido',
    confianza_ia DECIMAL(5,4),
    patologia VARCHAR(50) DEFAULT 'Ninguna',
    meta_calorica_diaria INT,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    es_apto_hipertenso BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permisos_roles (
    id_permiso SERIAL PRIMARY KEY,
    id_rol INT NOT NULL REFERENCES roles(id_rol),
    id_modulo INT NOT NULL REFERENCES modulos(id_modulo),
    puede_leer BOOLEAN DEFAULT TRUE,
    puede_escribir BOOLEAN DEFAULT FALSE,
    puede_editar BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE registro_consumo (
    id_registro SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    id_alimento INT NOT NULL REFERENCES alimentos(id_alimento),
    cantidad_gramos DECIMAL(6,2) NOT NULL,
    fecha_consumo DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'Registrado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE historial_chat (
    id_chat SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario),
    pregunta_usuario TEXT,
    respuesta_ia TEXT,
    flag_revision_nutricionista BOOLEAN DEFAULT FALSE,
    estado VARCHAR(20) DEFAULT 'Visible',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. INSERCIÓN DE DATOS (DML)

INSERT INTO roles (nombre_rol) VALUES ('Administrador'), ('Nutricionista'), ('Paciente');
INSERT INTO modulos (nombre_modulo) VALUES ('Mi Salud'), ('Gestión'), ('Soporte'), ('Maestros');

INSERT INTO permisos_roles (id_rol, id_modulo, puede_leer, puede_escribir) 
VALUES ((SELECT id_rol FROM roles WHERE nombre_rol = 'Paciente'), 1, TRUE, TRUE);

-- Usuarios de prueba (Actualizados con ubicación)
INSERT INTO usuarios (cedula, nombre_completo, email, genero, pais, departamento, ciudad, password_hash, id_rol) VALUES
('1010', 'Dr. Carlos Mendoza', 'carlos@nutri.com', 'Masculino', 'Colombia', 'Antioquia', 'Medellín', 'hash123', (SELECT id_rol FROM roles WHERE nombre_rol = 'Nutricionista')),
('777888999', 'Ana García', 'ana@paciente.com', 'Femenino', 'Colombia', 'Atlántico', 'Barranquilla', 'hash456', (SELECT id_rol FROM roles WHERE nombre_rol = 'Paciente'));

-- Perfil Clínico
INSERT INTO perfiles_clinicos (id_usuario, edad, peso_kg, altura_cm, biotipo, confianza_ia, meta_calorica_diaria) 
VALUES ((SELECT id_usuario FROM usuarios WHERE cedula = '777888999'), 28, 65.50, 168.00, 'Mesomorfo', 0.9850, 2100);

-- Alimentos
INSERT INTO alimentos (nombre, categoria, calorias, proteinas_g, carbohidratos_g, grasas_g, es_apto_diabetico) VALUES 
('Pechuga de Pollo', 'Proteínas', 165, 31.00, 0.00, 3.60, TRUE),
('Yogurt Griego', 'Lácteos', 59, 10.00, 3.60, 0.40, TRUE),
('Arroz Blanco', 'Carbohidratos', 130, 2.70, 28.00, 0.30, TRUE);

-- Registro de Consumo
INSERT INTO registro_consumo (id_usuario, id_alimento, cantidad_gramos) 
VALUES (
    (SELECT id_usuario FROM usuarios WHERE cedula = '777888999'),
    (SELECT id_alimento FROM alimentos WHERE nombre = 'Pechuga de Pollo'),
    200.00
);