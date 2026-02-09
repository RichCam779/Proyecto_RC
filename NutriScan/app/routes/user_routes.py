from fastapi import APIRouter, HTTPException
import requests  # Asegúrate de tener instalado: pip install requests
from app.controllers.user_controller import UserController
from app.models.user_model import User, BiotypeUpdate
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

user_controller = UserController()

# ---------------------------------------------------------
# CONFIGURACIÓN DEL MICROSERVICIO EXTERNO (Node.js)
# Pega aquí la URL que te dio Vercel para el servicio de ubicaciones
# Ejemplo: "https://servicio-geo-tu-nombre.vercel.app/api/ubicaciones"
NODE_SERVICE_URL = "https://proyecto-rc-jju7-mbe5fe4en-richcams-projects.vercel.app/api/ubicaciones" 
# ---------------------------------------------------------

@router.get("/locations")
def get_locations():
    """
    Endpoint Proxy: Consulta el microservicio de Node.js 
    y devuelve las ciudades disponibles al Frontend.
    """
    try:
        response = requests.get(NODE_SERVICE_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=502, detail="Error en el servicio de ubicaciones externo")
    except Exception as e:
        print(f"Error conectando con Node: {str(e)}")
        raise HTTPException(status_code=503, detail="El servicio de ubicaciones no responde")

@router.post("/", response_model=dict)
def create_user(user: User):
    return user_controller.create_user(user)

@router.get("/", response_model=dict)
def get_active_users():
    return user_controller.get_active_users()

@router.put("/{user_id}", response_model=dict)
def update_user(user_id: int, user: User):
    user.id = user_id
    return user_controller.update_user(user)

@router.delete("/{user_id}", response_model=dict)
def deactivate_user(user_id: int):
    return user_controller.deactivate_user(user_id)

@router.put("/{user_id}/biotype")
def update_biotype(user_id: int, data: BiotypeUpdate): 
    return user_controller.update_biotype(user_id, data.biotipo, data.confianza_ia)