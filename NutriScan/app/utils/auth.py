from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import HTTPException, status
from starlette.requests import Request
from dotenv import load_dotenv

load_dotenv()

# Configuración
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu_clave_secreta_super_segura_cambiar_en_produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos Pydantic para autenticación
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str

class SimpleTokenResponse(BaseModel):
    """Respuesta simple de autenticación con solo el token"""
    access: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Funciones de utilidad
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash o con texto plano (fallback temporal)"""
    try:
        # Intenta verificar como hash bcrypt
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Si falla, permite contraseñas en texto plano (fallback temporal para migracion)
        # IMPORTANTE: Esto es solo temporal. Migrar todos los passwords a bcrypt
        return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(request: Request) -> TokenData:
    """Verifica el token JWT desde el header Authorization"""
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autenticación. Use: Authorization: Bearer {token}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Intenta separar "Bearer token"
        parts = auth_header.split()
        
        if len(parts) == 2:
            scheme, token = parts
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Esquema de autenticación inválido. Use: Bearer {token}",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        elif len(parts) == 1:
            # Si solo hay una parte, asumimos que es el token sin "Bearer"
            token = parts[0]
        else:
            raise ValueError("Formato inválido")
            
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de header Authorization inválido. Use: Authorization: Bearer {token}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id_str is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: datos de usuario faltantes",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convierte user_id de string a int
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID de usuario malformado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return TokenData(user_id=user_id, email=email)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No se pudo validar el token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

