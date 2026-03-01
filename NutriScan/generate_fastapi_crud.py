import os

tables = [
    {"name": "roles", "id_col": "id_rol"},
    {"name": "modulos", "id_col": "id_modulo"},
    {"name": "telefono", "id_col": "id_telefono"},
    {"name": "perfiles_clinicos", "id_col": "id_perfil"},
    {"name": "alimentos", "id_col": "id_alimento"},
    {"name": "permisos_roles", "id_col": "id_permiso"},
    {"name": "registro_consumo", "id_col": "id_registro"},
    {"name": "historial", "id_col": "id_historial"},
    {"name": "historial_chat", "id_col": "id_chat"}
]

base_dir = r"c:\Proyecto_RCG\Proyecto_RC\NutriScan\app"

for t in tables:
    name = t["name"]
    id_col = t["id_col"]
    
    # Model (Generic Dict representation to avoid massive boilerplate, but FastAPI accepts dicts)
    model_code = f"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class {name.capitalize()}Create(BaseModel):
    data: Dict[str, Any]

class {name.capitalize()}Update(BaseModel):
    data: Dict[str, Any]
"""
    with open(os.path.join(base_dir, f"models/{name}_model.py"), "w", encoding="utf-8") as f:
        f.write(model_code)
        
    # Controller
    controller_code = f"""
import psycopg2
from fastapi import HTTPException
from app.config.db_config import get_db_connection
from datetime import datetime

class {name.capitalize()}Controller:
    
    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Revisar si existe la columna de estado para filtrar
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{name}' AND column_name='estado'")
            has_estado = cursor.fetchone() is not None
            
            if has_estado:
                cursor.execute("SELECT * FROM {name} WHERE estado != 'Inactivo' ORDER BY {id_col} ASC")
            else:
                cursor.execute("SELECT * FROM {name} ORDER BY {id_col} ASC")
                
            columns = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
            
            return {{"resultado": [dict(zip(columns, row)) for row in result]}}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def get_by_id(self, item_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM {name} WHERE {id_col} = %s", (item_id,))
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No encontrado")
            return {{"resultado": dict(zip(columns, row))}}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()
            
    def create(self, data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Aseguramos de insertar la fecha actual
            if 'crear' not in data:
                data['crear'] = datetime.now()
            if 'actualizar' not in data:
                data['actualizar'] = datetime.now()
                
            keys = list(data.keys())
            values = tuple(data.values())
            
            placeholders = ", ".join(["%s"] * len(keys))
            columns = ", ".join(keys)
            
            query = f"INSERT INTO {name} ({{columns}}) VALUES ({{placeholders}}) RETURNING *"
            cursor.execute(query, values)
            
            cols = [desc[0] for desc in cursor.description]
            new_row = cursor.fetchone()
            
            conn.commit()
            return {{"resultado": "Creado con éxito", "data": dict(zip(cols, new_row))}}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update(self, item_id: int, data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Forzar actualización de fecha
            data['actualizar'] = datetime.now()
            
            keys = list(data.keys())
            values = list(data.values())
            
            set_clause = ", ".join([f"{{k}} = %s" for k in keys])
            values.append(item_id)
            
            query = f"UPDATE {name} SET {{set_clause}} WHERE {id_col} = %s RETURNING *"
            cursor.execute(query, tuple(values))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="No encontrado")
                
            cols = [desc[0] for desc in cursor.description]
            updated_row = cursor.fetchone()
                
            conn.commit()
            return {{"resultado": "Actualizado con éxito", "data": dict(zip(cols, updated_row))}}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def delete(self, item_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{name}' AND column_name='estado'")
            has_estado = cursor.fetchone() is not None
            
            if has_estado:
                cursor.execute(f"UPDATE {name} SET estado = 'Inactivo', actualizar = NOW() WHERE {id_col} = %s", (item_id,))
            else:
                cursor.execute(f"DELETE FROM {name} WHERE {id_col} = %s", (item_id,))
                
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="No encontrado")
                
            conn.commit()
            return {{"resultado": "Eliminado o desactivado con éxito"}}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()
"""
    with open(os.path.join(base_dir, f"controllers/{name}_controller.py"), "w", encoding="utf-8") as f:
        f.write(controller_code)
        
    # Route
    route_code = f"""
from fastapi import APIRouter, Request, HTTPException
from app.controllers.{name}_controller import {name.capitalize()}Controller
from app.models.{name}_model import {name.capitalize()}Create, {name.capitalize()}Update
from app.utils.auth import verify_token

router = APIRouter(
    prefix="/{name}",
    tags=["{name}"]
)

controller = {name.capitalize()}Controller()

@router.get("/")
async def get_all(request: Request):
    await verify_token(request)
    return controller.get_all()

@router.get("/{{item_id}}")
async def get_by_id(item_id: int, request: Request):
    await verify_token(request)
    return controller.get_by_id(item_id)

@router.post("/")
async def create(data: {name.capitalize()}Create, request: Request):
    await verify_token(request)
    return controller.create(data.data)

@router.put("/{{item_id}}")
async def update(item_id: int, data: {name.capitalize()}Update, request: Request):
    await verify_token(request)
    return controller.update(item_id, data.data)

@router.delete("/{{item_id}}")
async def delete(item_id: int, request: Request):
    await verify_token(request)
    return controller.delete(item_id)
"""
    with open(os.path.join(base_dir, f"routes/{name}_routes.py"), "w", encoding="utf-8") as f:
        f.write(route_code)

print("¡Archivos generados con éxito!")
