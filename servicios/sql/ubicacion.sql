-- =============================================================
-- MÓDULO DE UBICACIONES (CORREGIDO Y ESTANDARIZADO)
-- =============================================================

-- 1. LIMPIEZA
DROP TRIGGER IF EXISTS trigger_update_ciudades ON ciudades;
DROP TRIGGER IF EXISTS trigger_update_departamentos ON departamentos;
DROP TRIGGER IF EXISTS trigger_update_paises ON paises;
DROP TABLE IF EXISTS ciudades CASCADE;
DROP TABLE IF EXISTS departamentos CASCADE;
DROP TABLE IF EXISTS paises CASCADE;
DROP FUNCTION IF EXISTS actualizar_fecha_modificacion CASCADE;

-- 2. FUNCIÓN DE AUTOMATIZACIÓN (Compatible con todas las tablas)
CREATE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    -- Usamos updated_at para que coincida con la tabla de usuarios
    NEW.updated_at = NOW(); 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- =============================================================
-- 3. CREACIÓN DE TABLAS + TRIGGERS
-- =============================================================

-- TABLA PAISES
CREATE TABLE paises (
    id_pais SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- CORREGIDO
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- CORREGIDO
);

CREATE TRIGGER trigger_update_paises
BEFORE UPDATE ON paises
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA DEPARTAMENTOS
CREATE TABLE departamentos (
    id_departamento SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_pais INT NOT NULL REFERENCES paises(id_pais) ON DELETE CASCADE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- CORREGIDO
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- CORREGIDO
);

CREATE TRIGGER trigger_update_departamentos
BEFORE UPDATE ON departamentos
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA CIUDADES
CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_departamento INT NOT NULL REFERENCES departamentos(id_departamento) ON DELETE CASCADE,
    estado VARCHAR(20) DEFAULT 'Activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- CORREGIDO
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- CORREGIDO
);

CREATE TRIGGER trigger_update_ciudades
BEFORE UPDATE ON ciudades
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion();

-- =============================================================
-- 4. DATOS DE PRUEBA
-- =============================================================

INSERT INTO paises (nombre) VALUES 
('Colombia'), ('México'), ('Argentina'), ('España'), ('Estados Unidos');

INSERT INTO departamentos (nombre, id_pais) VALUES 
('Antioquia', 1), ('Cundinamarca', 1),
('Jalisco', 2), ('CDMX', 2),
('Buenos Aires', 3), ('Córdoba', 3),
('Madrid', 4), ('Cataluña', 4),
('Florida', 5), ('Texas', 5);

INSERT INTO ciudades (nombre, id_departamento) VALUES 
('Medellín', 1), ('Bogotá', 2),
('Guadalajara', 3), ('Ciudad de México', 4),
('La Plata', 5), ('Córdoba Capital', 6),
('Madrid', 7), ('Barcelona', 8),
('Miami', 9), ('Houston', 10);