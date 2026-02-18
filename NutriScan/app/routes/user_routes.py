from fastapi import APIRouter, HTTPException, Request
import requests
from app.controllers.user_controller import UserController
from app.models.user_model import User, BiotypeUpdate
from app.utils.auth import verify_token, TokenData
from typing import List
import os

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()

# URL del servicio de ubicaciones
NODE_SERVICE_URL = os.getenv("NODE_SERVICE_URL", "https://proyecto-rc-jju7.vercel.app/api/ubicaciones") 

# Proxy para obtener ciudades
@router.get("/locations")
def get_external_locations():
    try:
        response = requests.get(NODE_SERVICE_URL, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail="El servicio de ubicaciones devolvió un error."
            )
            
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Tiempo de espera agotado.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Error de conexión.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


# Rutas CRUD de usuarios

# Crear usuario
@router.post("/", response_model=dict)
async def create_user(user: User, request: Request):
    current_user = await verify_token(request)
    return user_controller.create_user(user)

# Obtener usuarios activos
@router.get("/", response_model=dict)
async def get_active_users(request: Request):
    current_user = await verify_token(request)
    return user_controller.get_active_users()

# Actualizar usuario
@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, user: User, request: Request):
    current_user = await verify_token(request)
    user.id = user_id
    return user_controller.update_user(user)

# Desactivar usuario
@router.delete("/{user_id}", response_model=dict)
async def deactivate_user(user_id: int, request: Request):
    current_user = await verify_token(request)
    return user_controller.deactivate_user(user_id)

# Actualizar biotipo
@router.put("/{user_id}/biotype")
async def update_biotype(user_id: int, data: BiotypeUpdate, request: Request): 
    current_user = await verify_token(request)
    return user_controller.update_biotype(user_id, data.biotipo, data.confianza_ia)
