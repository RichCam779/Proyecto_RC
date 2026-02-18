from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Modelo de usuario
class User(BaseModel):
    id: Optional[int] = None
    
    # Datos personales
    cedula: str
    nombre_completo: str
    email: EmailStr
    genero: str
    
    # Ubicación
    pais: str
    departamento: str
    ciudad: str
    
    # Contacto y seguridad
    telefono: Optional[str] = None
    password_hash: str
    id_rol: int
    
    # Auditoría
    estado: Optional[str] = "Activo"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelo para actualización de biotipo
class BiotypeUpdate(BaseModel):
    biotipo: str
    confianza_ia: float