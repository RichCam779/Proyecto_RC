
from fastapi import APIRouter, Request, HTTPException
from app.controllers.perfiles_clinicos_controller import Perfiles_clinicosController
from app.models.perfiles_clinicos_model import Perfiles_clinicosCreate, Perfiles_clinicosUpdate
from app.utils.auth import verify_token

router = APIRouter(
    prefix="/perfiles_clinicos",
    tags=["perfiles_clinicos"]
)

controller = Perfiles_clinicosController()

@router.get("/")
async def get_all(request: Request):
    await verify_token(request)
    return controller.get_all()

@router.get("/{item_id}")
async def get_by_id(item_id: int, request: Request):
    await verify_token(request)
    return controller.get_by_id(item_id)

@router.post("/")
async def create(data: Perfiles_clinicosCreate, request: Request):
    await verify_token(request)
    return controller.create(data.data)

@router.put("/{item_id}")
async def update(item_id: int, data: Perfiles_clinicosUpdate, request: Request):
    await verify_token(request)
    return controller.update(item_id, data.data)

@router.delete("/{item_id}")
async def delete(item_id: int, request: Request):
    await verify_token(request)
    return controller.delete(item_id)
