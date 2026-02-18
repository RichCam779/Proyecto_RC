import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.config.db_config import get_db_connection
from app.models.user_model import User
from app.utils.auth import verify_password

# Controlador de usuarios
class UserController:
    
    # Crear usuario y perfil clínico
    def create_user(self, user: User):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO usuarios 
                (cedula, nombre_completo, email, genero, pais, departamento, ciudad, password_hash, id_rol) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING id_usuario
            """
            values = (
                user.cedula, 
                user.nombre_completo, 
                user.email, 
                user.genero,
                user.pais,
                user.departamento,
                user.ciudad,
                user.password_hash, 
                user.id_rol
            )
            
            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]

            # Insertar teléfono
            if user.telefono:
                cursor.execute("INSERT INTO telefono (id_usuario, numero, tipo) VALUES (%s, %s, 'Movil')", (new_id, user.telefono))
            
            # Crear perfil clínico vacío
            cursor.execute("INSERT INTO perfiles_clinicos (id_usuario) VALUES (%s)", (new_id,))
            
            conn.commit()
            return {"resultado": "Usuario y Perfil creados con éxito", "id": new_id}
        
        except psycopg2.Error as err:
            if conn: conn.rollback()
            if err.pgcode == '23505':
                raise HTTPException(status_code=400, detail="Error: Ya existe un usuario con esa cédula o email.")
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(err)}")
        finally:
            if conn: conn.close()

    # Obtener lista de usuarios activos
    def get_active_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT DISTINCT ON (u.id_usuario) 
                    u.id_usuario, 
                    u.cedula, 
                    u.nombre_completo, 
                    u.email, 
                    t.numero AS telefono, 
                    u.genero, 
                    u.pais, 
                    u.departamento, 
                    u.ciudad, 
                    r.nombre_rol, 
                    pc.biotipo, 
                    u.estado, 
                    u.created_at
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                LEFT JOIN perfiles_clinicos pc ON u.id_usuario = pc.id_usuario
                LEFT JOIN telefono t ON u.id_usuario = t.id_usuario AND t.estado = 'Activo'
                WHERE u.estado = 'Activo'
            """
            cursor.execute(query)
            result = cursor.fetchall()
            
            payload = []
            for data in result:
                content = {
                    'id': data[0], 
                    'cedula': data[1], 
                    'nombre': data[2],
                    'email': data[3], 
                    'telefono': data[4] if data[4] else "Sin registro",
                    'genero': data[5], 
                    'pais': data[6] if data[6] else "No definido",
                    'departamento': data[7] if data[7] else "No definido",
                    'ciudad': data[8] if data[8] else "No definido",
                    'rol': data[9], 
                    'biotipo': data[10], 
                    'estado': data[11],
                    'created_at': data[12]
                }
                payload.append(content)
            
            return {"resultado": jsonable_encoder(payload)}
                
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    # Actualizar datos de usuario
    def update_user(self, user: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE usuarios 
                SET nombre_completo = %s, email = %s, genero = %s, 
                    pais = %s, departamento = %s, ciudad = %s,
                    password_hash = %s, id_rol = %s
                WHERE id_usuario = %s
            """
            values = (
                user.nombre_completo, 
                user.email, 
                user.genero,
                user.pais,
                user.departamento,
                user.ciudad,
                user.password_hash, 
                user.id_rol, 
                user.id
            )

            cursor.execute(query, values)

            # Actualizar o insertar teléfono
            if user.telefono:
                cursor.execute("SELECT id_telefono FROM telefono WHERE id_usuario = %s", (user.id,))
                existing_phone = cursor.fetchone()
                
                if existing_phone:
                    cursor.execute("UPDATE telefono SET numero = %s WHERE id_telefono = %s", (user.telefono, existing_phone[0]))
                else:
                    cursor.execute("INSERT INTO telefono (id_usuario, numero, tipo) VALUES (%s, %s, 'Movil')", (user.id, user.telefono))
            
            conn.commit()
            return {"resultado": "Usuario actualizado con éxito"}
            
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    # Desactivar cuenta de usuario
    def deactivate_user(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET estado = 'Inactivo' WHERE id_usuario = %s", (user_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
                
            return {"resultado": "Cuenta de usuario desactivada correctamente"}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    # Actualizar biotipo del perfil clínico
    def update_biotype(self, user_id: int, biotipo: str, confianza: float):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE perfiles_clinicos 
                SET biotipo = %s, confianza_ia = %s 
                WHERE id_usuario = %s
            """, (biotipo, confianza, user_id))
            conn.commit()
            return {"resultado": "Biotipo actualizado por IA"}
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    # Autenticar usuario por email y contraseña
    def authenticate_user(self, email: str, password: str):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT id_usuario, email, password_hash, nombre_completo, id_rol, estado
                FROM usuarios
                WHERE email = %s AND estado = 'Activo'
            """
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
            
            user_id, user_email, hashed_password, nombre, rol, estado = result
            
            if not verify_password(password, hashed_password):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")
            
            return {
                "id": user_id,
                "email": user_email,
                "nombre": nombre,
                "id_rol": rol
            }
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(err)}")
        finally:
            if conn: conn.close()
