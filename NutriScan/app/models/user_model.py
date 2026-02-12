from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    # Campos opcionales (para actualizaciones o lecturas parciales)
    id: Optional[int] = None
    
    # Datos Personales
    cedula: str
    nombre_completo: str
    email: EmailStr
    genero: str
    
    # UBICACIÓN:
    # Ajustado para coincidir con la base de datos actual (que usa texto)
    pais: str
    departamento: str
    ciudad: str
    # id_ciudad: int  <-- Deshabilitado hasta que la BD tenga la tabla ciudades    
    # Contacto y Seguridad
    telefono: Optional[str] = None
    password_hash: str
    id_rol: int
    
    # Campos de Auditoría (Solo lectura, no se envían al crear)
    estado: Optional[str] = "Activo"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelo exclusivo para cuando actualizas solo el biotipo (ese está bien, déjalo igual)
class BiotypeUpdate(BaseModel):
    biotipo: str
    confianza_ia: float