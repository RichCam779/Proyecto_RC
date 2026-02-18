from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import HTTPException, status
from starlette.requests import Request
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_super_segura_cambiar_en_produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos para autenticación
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str

class SimpleTokenResponse(BaseModel):
    access: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Funciones de utilidad

# Verificar contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return plain_password == hashed_password

# Generar hash
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Crear token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar token JWT
async def verify_token(request: Request) -> TokenData:
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        parts = auth_header.split()
        if len(parts) == 2:
            scheme, token = parts
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Esquema inválido")
        elif len(parts) == 1:
            token = parts[0]
        else:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id_str is None or email is None:
            raise HTTPException(status_code=401, detail="Token incompleto")
        
        return TokenData(user_id=int(user_id_str), email=email)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

