-- =============================================================
-- MÓDULO DE UBICACIONES (CON AUDITORÍA AUTOMÁTICA)
-- =============================================================

-- 1. LIMPIEZA PREVIA
DROP TRIGGER IF EXISTS trigger_update_ciudades ON ciudades;
DROP TRIGGER IF EXISTS trigger_update_departamentos ON departamentos;
DROP TRIGGER IF EXISTS trigger_update_paises ON paises;
DROP TABLE IF EXISTS ciudades CASCADE;
DROP TABLE IF EXISTS departamentos CASCADE;
DROP TABLE IF EXISTS paises CASCADE;
DROP FUNCTION IF EXISTS actualizar_fecha_modificacion CASCADE;

-- 2. FUNCIÓN DE AUTOMATIZACIÓN (Para que actualizar cambie solo)
CREATE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizar = NOW(); -- Asigna la hora actual al campo actualizar
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
    crear TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Se guarda solo al crear
    actualizar TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Se guarda al crear y cambia al editar
);

-- Trigger para Paises (Activa la función al editar)
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
    crear TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para Departamentos
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
    crear TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para Ciudades
CREATE TRIGGER trigger_update_ciudades
BEFORE UPDATE ON ciudades
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion();

-- =============================================================
-- 4. INSERCIÓN DE DATOS DE PRUEBA (10 REGISTROS)
-- =============================================================

-- Paises
INSERT INTO paises (nombre) VALUES 
('Colombia'), ('México'), ('Argentina'), ('España'), ('Estados Unidos');

-- Departamentos (Asumiendo IDs 1 a 5)
INSERT INTO departamentos (nombre, id_pais) VALUES 
('Antioquia', 1), ('Cundinamarca', 1), -- Colombia
('Jalisco', 2), ('CDMX', 2),           -- México
('Buenos Aires', 3), ('Córdoba', 3),   -- Argentina
('Madrid', 4), ('Cataluña', 4),        -- España
('Florida', 5), ('Texas', 5);          -- USA

-- Ciudades
INSERT INTO ciudades (nombre, id_departamento) VALUES 
('Medellín', 1), ('Bogotá', 2),
('Guadalajara', 3), ('Ciudad de México', 4),
('La Plata', 5), ('Córdoba Capital', 6),
('Madrid', 7), ('Barcelona', 8),
('Miami', 9), ('Houston', 10);
-- =============================================================
