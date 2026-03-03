from fastapi import HTTPException, UploadFile
from app.utils.ai_utils import YOLOHandler
from app.controllers.perfiles_clinicos_controller import Perfiles_clinicosController
from app.controllers.alimentos_controller import AlimentosController
from app.controllers.registro_consumo_controller import Registro_consumoController
from datetime import datetime
import os

class AIController:
    def __init__(self):
        # El modelo se cargará/descargará al iniciar el controlador
        self.yolo = YOLOHandler()
        self.perfil_controller = Perfiles_clinicosController()
        self.alimento_controller = AlimentosController()
        self.consumo_controller = Registro_consumoController()

    async def analyze_biotype(self, user_id: int, file: UploadFile):
        # Leer el contenido del archivo
        image_bytes = await file.read()
        
        # Ejecutar análisis
        biotype, confidence = self.yolo.detect_and_analyze_biotype(image_bytes)
        
        if not biotype:
            raise HTTPException(status_code=400, detail="No se pudo detectar una persona en la foto")
            
        # Buscar perfil clínico del usuario
        try:
            # Intentar actualizar el biótipo del usuario
            # Nota: Necesitamos el ID del perfil, el controller de perfiles busca por id_perfil
            # Pero podemos usar una consulta SQL directa aquí o mejorar el controller.
            # Vamos a usar una lógica para buscar el ID de perfil por id_usuario.
            
            # Para fines de demostración, asumiremos que el controller de perfiles
            # tiene un método para actualizar por id_usuario o buscaremos el ID primero.
            
            # Buscamos el ID del perfil clínico asignado a este usuario
            from app.config.db_config import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id_perfil FROM perfiles_clinicos WHERE id_usuario = %s", (user_id,))
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="El usuario no tiene un perfil clínico creado")
            
            id_perfil = row[0]
            
            # Actualizamos
            data_to_update = {
                "biotipo": biotype,
                "confianza_ia": confidence,
                "fecha_actualizacion": datetime.now()
            }
            self.perfil_controller.update(id_perfil, data_to_update)
            conn.close()
            
            return {
                "resultado": "Análisis completado",
                "biotipo_detectado": biotype,
                "confianza": f"{confidence:.2f}%"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar biótipo: {str(e)}")

    async def analyze_food(self, user_id: int, file: UploadFile):
        image_bytes = await file.read()
        
        # Detectar comidas
        detections = self.yolo.detect_food(image_bytes)
        
        if not detections:
            raise HTTPException(status_code=400, detail="No se detectaron alimentos reconocibles")
            
        # Tomar la detección con mayor confianza
        best_detection = max(detections, key=lambda x: x["confidence"])
        label = best_detection["label"]
        
        # Buscar el alimento en nuestra BD para obtener calorías reales
        from app.config.db_config import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Búsqueda difusa por el nombre del label de YOLO (traducido o mapeado)
        food_translations = {
            "apple": "Manzana",
            "banana": "Banano",
            "orange": "Naranja",
            "sandwich": "Sandwich",
            "broccoli": "Brocoli",
            "pizza": "Pizza",
            "cake": "Pastel",
            "donut": "Dona",
            "hot dog": "Perro Caliente",
            "carrot": "Zanahoria"
        }
        
        translated_name = food_translations.get(label, label)
        cursor.execute("SELECT * FROM alimentos WHERE nombre ILIKE %s AND estado = 'Activo' LIMIT 1", (f"%{translated_name}%",))
        columns = [desc[0] for desc in cursor.description]
        food_db = cursor.fetchone()
        
        if not food_db:
             conn.close()
             return {
                "label": label,
                "confidence": best_detection["confidence"],
                "mensaje": "Alimento reconocido por IA pero no está en nuestro inventario de calorías.",
                "calorias_estimadas": 0
            }
            
        food_data = dict(zip(columns, food_db))
        
        # Registrar consumo automático si se desea (o solo devolver la info)
        # Por ahora solo devolvemos la info para confirmación del usuario
        
        conn.close()
        return {
            "alimento_detectado": food_data["nombre"],
            "calorias": food_data["calorias"],
            "proteinas": food_data["proteinas_g"],
            "carbohidratos": food_data["carbohidratos_g"],
            "grasas": food_data["grasas_g"],
            "confianza_ia": best_detection["confidence"]
        }
