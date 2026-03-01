
from fastapi import APIRouter, Request, HTTPException
from app.controllers.historial_chat_controller import Historial_chatController
from app.models.historial_chat_model import Historial_chatCreate, Historial_chatUpdate
from app.utils.auth import verify_token

router = APIRouter(
    prefix="/historial_chat",
    tags=["historial_chat"]
)

controller = Historial_chatController()

@router.get("/")
async def get_all(request: Request):
    await verify_token(request)
    return controller.get_all()

@router.get("/{item_id}")
async def get_by_id(item_id: int, request: Request):
    await verify_token(request)
    return controller.get_by_id(item_id)

@router.post("/")
async def create(data: Historial_chatCreate, request: Request):
    await verify_token(request)
    return controller.create(data.data)

@router.put("/{item_id}")
async def update(item_id: int, data: Historial_chatUpdate, request: Request):
    await verify_token(request)
    return controller.update(item_id, data.data)

@router.delete("/{item_id}")
async def delete(item_id: int, request: Request):
    await verify_token(request)
    return controller.delete(item_id)
