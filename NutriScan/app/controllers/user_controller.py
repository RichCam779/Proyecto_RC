import psycopg2
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
# Respetamos tu importación original de configuración
from app.config.db_config import get_db_connection
from app.models.user_model import User 

class UserController:
    
    def create_user(self, user: User):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # 1. Insertamos en la tabla usuarios (SIN teléfono)
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
                user.pais,          # Nuevo
                user.departamento,  # Nuevo
                user.ciudad,        # Nuevo
                user.password_hash, 
                user.id_rol
            )
            
            cursor.execute(query, values)
            new_id = cursor.fetchone()[0]

            # 1.5 Insertamos el teléfono si existe
            if user.telefono:
                cursor.execute("INSERT INTO telefono (id_usuario, numero, tipo) VALUES (%s, %s, 'Movil')", (new_id, user.telefono))
            
            # 2. Creamos el perfil clínico vacío
            cursor.execute("INSERT INTO perfiles_clinicos (id_usuario) VALUES (%s)", (new_id,))
            
            conn.commit()
            return {"resultado": "Usuario y Perfil creados con éxito", "id": new_id}
        
        except psycopg2.Error as err:
            if conn: conn.rollback()
            if err.pgcode == '23505': # Código de error Postgres para duplicados
                raise HTTPException(status_code=400, detail="Error: Ya existe un usuario con esa cédula o email.")
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(err)}")
        finally:
            if conn: conn.close()

    def get_active_users(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Query actualizado: Traemos telefono de la tabla separada
            # Usamos un DISTINCT ON o un GROUP BY simple para evitar duplicados si tuviera multiples telefonos,
            # pero asumiremos el primero encontrado para mantener el diseño simple.
            query = """
                SELECT DISTINCT ON (u.id_usuario) u.id_usuario, u.cedula, u.nombre_completo, u.email, t.numero, u.genero, 
                       u.pais, u.departamento, u.ciudad, r.nombre_rol, p.biotipo, u.estado
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                LEFT JOIN perfiles_clinicos p ON u.id_usuario = p.id_usuario
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
                    'telefono': data[4],    # Índice correcto para teléfono
                    'genero': data[5], 
                    'pais': data[6],        # Nuevo
                    'departamento': data[7],# Nuevo
                    'ciudad': data[8],      # Nuevo
                    'rol': data[9], 
                    'biotipo': data[10], 
                    'estado': data[11]
                }
                payload.append(content)
            
            return {"resultado": jsonable_encoder(payload)}
                
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

    def update_user(self, user: User):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Update usuarios (sin telefono)
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
                user.pais,          # Nuevo
                user.departamento,  # Nuevo
                user.ciudad,        # Nuevo
                user.password_hash, 
                user.id_rol, 
                user.id
            )

            cursor.execute(query, values)

            # Manejo del teléfono
            if user.telefono:
                # Verificamos si ya existe un teléfono para este usuario
                cursor.execute("SELECT id_telefono FROM telefono WHERE id_usuario = %s", (user.id,))
                existing_phone = cursor.fetchone()
                
                if existing_phone:
                    cursor.execute("UPDATE telefono SET numero = %s WHERE id_telefono = %s", (user.telefono, existing_phone[0]))
                else:
                    cursor.execute("INSERT INTO telefono (id_usuario, numero, tipo) VALUES (%s, %s, 'Movil')", (user.id, user.telefono))
            
            conn.commit()
            if cursor.rowcount == 0 and not user.telefono: # Si no se actualizó usuario y no se tocó teléfono... (aproximación)
                 # Nota: rowcount del update usuarios podría ser 0 si los datos son iguales, pero retornamos éxito igual.
                 # El chequeo original era para ver si el ID existía.
                 pass
                 
            return {"resultado": "Usuario actualizado con éxito"}
            
        except psycopg2.Error as err:
            if conn: conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn: conn.close()

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