-- =============================================================
-- SQL DE GEOGRAFÍA (SERVICIO EXTERNO)
-- =============================================================

-- FUNCIÓN DE ACTUALIZACIÓN AUTOMÁTICA
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TABLA PAISES
CREATE TABLE paises (
    id_pais SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_paises BEFORE UPDATE ON paises FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA DEPARTAMENTOS
CREATE TABLE departamentos (
    id_departamento SERIAL PRIMARY KEY,
    id_pais INT NOT NULL REFERENCES paises(id_pais) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_departamentos BEFORE UPDATE ON departamentos FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- TABLA CIUDADES
CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    id_departamento INT NOT NULL REFERENCES departamentos(id_departamento) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER trigger_update_ciudades BEFORE UPDATE ON ciudades FOR EACH ROW EXECUTE FUNCTION actualizar_fecha_modificacion();

-- =============================================================
-- INSERCIÓN DE DATOS INICIALES
-- =============================================================

INSERT INTO paises (nombre) VALUES 
('Colombia'), ('Mexico'), ('Argentina'), ('Chile'), ('Peru');

INSERT INTO departamentos (id_pais, nombre) VALUES 
(1, 'Bogota'), (1, 'Antioquia'), (1, 'Valle del Cauca'), (1, 'Atlantico'),
(2, 'Ciudad de Mexico'), (2, 'Jalisco'), (2, 'Nuevo Leon'),
(3, 'Buenos Aires'), (3, 'Cordoba'), (3, 'Santa Fe');

INSERT INTO ciudades (id_departamento, nombre) VALUES 
(1, 'Bogota'), (2, 'Medellin'), (2, 'Envigado'), (3, 'Cali'), (3, 'Palmira'), (4, 'Barranquilla'),
(5, 'CDMX'), (6, 'Guadalajara'), (7, 'Monterrey'),
(8, 'Buenos Aires'), (9, 'Cordoba'), (10, 'Rosario');
