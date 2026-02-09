from fastapi import APIRouter, HTTPException
import requests  # Importante: Asegúrate de que 'requests' esté en requirements.txt
from app.controllers.user_controller import UserController
from app.models.user_model import User, BiotypeUpdate
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
NODE_SERVICE_URL = "https://tu-servicio-node.vercel.app/api/ubicaciones" 

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
def create_user(user: User):
    return user_controller.create_user(user)

@router.get("/", response_model=dict)
def get_active_users():
    return user_controller.get_active_users()

@router.put("/{user_id}", response_model=dict)
def update_user(user_id: int, user: User):
    # Asignamos el ID del path al objeto user para el controlador
    user.id = user_id
    return user_controller.update_user(user)

@router.delete("/{user_id}", response_model=dict)
def deactivate_user(user_id: int):
    return user_controller.deactivate_user(user_id)

@router.put("/{user_id}/biotype")
def update_biotype(user_id: int, data: BiotypeUpdate): 
    return user_controller.update_biotype(user_id, data.biotipo, data.confianza_ia)