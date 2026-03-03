from fastapi import APIRouter, UploadFile, File, HTTPException
from app.controllers.ai_controller import AIController

router = APIRouter(prefix="/ai", tags=["AI Analysis"])

# Instanciar el controlador de IA
# El modelo YOLOv8n se cargará una vez al arrancar (o al primer uso)
ai_controller = AIController()

@router.post("/biotype/{user_id}")
async def analyze_biotype(user_id: int, file: UploadFile = File(...)):
    """
    Recibe una foto de la persona y analiza su biótipo (Ectomorfo, Mesomorfo o Endomorfo).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida")
    
    return await ai_controller.analyze_biotype(user_id, file)

@router.post("/food-recognition/{user_id}")
async def analyze_food(user_id: int, file: UploadFile = File(...)):
    """
    Recibe una foto de alimento, lo identifica, devuelve calorías y macronutrientes 
    comparando con la tabla de 'alimentos' de la base de datos.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo no es una imagen válida")
        
    return await ai_controller.analyze_food(user_id, file)
