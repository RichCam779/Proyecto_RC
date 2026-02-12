from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    cedula: str
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None
    genero: Optional[str] = None
    pais: Optional[str] = None
    departamento: Optional[str] = None
    ciudad: Optional[str] = None
    password_hash: str
    id_rol: int
    crear: Optional[datetime] = None
    actualizar: Optional[datetime] = None

class BiotypeUpdate(BaseModel):
    biotipo: str
    confianza_ia: float

