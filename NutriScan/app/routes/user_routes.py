from fastapi import APIRouter, HTTPException, Request
import requests  # Importante: Asegúrate de que 'requests' esté en requirements.txt
from app.controllers.user_controller import UserController
from app.models.user_model import User, BiotypeUpdate
from app.utils.auth import verify_token, TokenData
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()

# ---------------------------------------------------------
# CONFIGURACIÓN DEL MICROSERVICIO (El Puente)
# ---------------------------------------------------------
# REEMPLAZA ESTO con la URL exacta de tu proyecto de Node.js en Vercel.
# Debe terminar en /api/ubicaciones
NODE_SERVICE_URL = "https://proyecto-rc-jju7.vercel.app/api/ubicaciones" 

@router.get("/locations")
def get_external_locations():
    """
    ENDPOINT PROXY:
    1. Recibe la petición del Frontend.
    2. Llama al Microservicio de Node.js.
    3. Devuelve la lista de ciudades.
    """
    try:
        # Hacemos la petición a Node.js con un tiempo de espera de 10 segundos
        response = requests.get(NODE_SERVICE_URL, timeout=10)
        
        # Si Node.js responde bien (Código 200)
        if response.status_code == 200:
            return response.json()
        else:
            # Si Node.js devuelve error (ej: 404 o 500)
            raise HTTPException(
                status_code=response.status_code, 
                detail="El servicio de ubicaciones devolvió un error."
            )
            
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="El servicio de ubicaciones tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="No se pudo conectar con el servicio de ubicaciones.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del proxy: {str(e)}")


# ---------------------------------------------------------
# RUTAS NORMALES DE USUARIO (CRUD)
# ---------------------------------------------------------

@router.post("/", response_model=dict)
async def create_user(user: User, request: Request):
    """
    Crear nuevo usuario. Requiere autenticación JWT.
    """
    current_user = await verify_token(request)
    return user_controller.create_user(user)

@router.get("/", response_model=dict)
async def get_active_users(request: Request):
    """
    Obtener usuarios activos. Requiere autenticación JWT.
    
    **Pasos:**
    1. POST /login con email y password
    2. Copia el token del campo "access"
    3. En Swagger: click en Authorize (arriba a la derecha)
    4. Pega el token sin el prefijo "Bearer"
    5. Luego haz GET /users/
    """
    current_user = await verify_token(request)
    return user_controller.get_active_users()

@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, user: User, request: Request):
    """
    Actualizar usuario. Requiere autenticación JWT.
    """
    current_user = await verify_token(request)
    # Asignamos el ID del path al objeto user para el controlador
    user.id = user_id
    return user_controller.update_user(user)

@router.delete("/{user_id}", response_model=dict)
async def deactivate_user(user_id: int, request: Request):
    """
    Desactivar usuario. Requiere autenticación JWT.
    """
    current_user = await verify_token(request)
    return user_controller.deactivate_user(user_id)

@router.put("/{user_id}/biotype")
async def update_biotype(user_id: int, data: BiotypeUpdate, request: Request): 
    """
    Actualizar biotipo del usuario. Requiere autenticación JWT.
    """
    current_user = await verify_token(request)
    return user_controller.update_biotype(user_id, data.biotipo, data.confianza_ia)