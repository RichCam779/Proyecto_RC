# 🔐 NutriScan API - Guía de Autenticación JWT

## Autenticación JWT Implementada ✅

La API ahora cuenta con autenticación segura mediante **JWT (JSON Web Tokens)**.

### 📋 Variables de Entorno Requeridas

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_bd
JWT_SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion
PORT=8000
```

> Ver archivo `.env.example` para más detalles.

---

## 🔑 Endpoints de Autenticación

### 1. **Login - Obtener Token**

**Endpoint:**
```
POST /auth/login
```

**Body (JSON):**
```json
{
  "email": "usuario@example.com",
  "password": "tu_contraseña"
}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "usuario@example.com"
}
```

**Errores:**
- `401 Unauthorized`: Credenciales inválidas o usuario inactivo

---

## 📌 Endpoints Protegidos

Los siguientes endpoints **requieren autenticación JWT**:

### Endpoints de Usuarios

- **POST** `/users/` - Crear usuario
- **GET** `/users/` - Obtener usuarios activos
- **PUT** `/users/{user_id}` - Actualizar usuario
- **DELETE** `/users/{user_id}` - Desactivar usuario
- **PUT** `/users/{user_id}/biotype` - Actualizar biotipo

### Endpoints Públicos

- **GET** `/` - Health check
- **GET** `/users/locations` - Obtener ubicaciones (proxy a Node.js)
- **POST** `/auth/login` - Login

---

## 🚀 Cómo Usar los Endpoints Protegidos

### 1. **Obtener Token**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.admin@app.com",
    "password": "pass1"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "juan.admin@app.com"
}
```

### 2. **Usar Token en Solicitud Protegida**

Inclúyelo en el header `Authorization`:

```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 3. **Ejemplo en Python (requests)**

```python
import requests

# 1. Login
response = requests.post(
    "http://localhost:8000/auth/login",
    json={
        "email": "juan.admin@app.com",
        "password": "pass1"
    }
)

token = response.json()["access_token"]

# 2. Usar token en solicitud protegida
headers = {"Authorization": f"Bearer {token}"}
users = requests.get("http://localhost:8000/users/", headers=headers)
print(users.json())
```

### 4. **Ejemplo en JavaScript/Fetch**

```javascript
// 1. Login
const loginResponse = await fetch("http://localhost:8000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "juan.admin@app.com",
    password: "pass1"
  })
});

const { access_token } = await loginResponse.json();

// 2. Usar token en solicitud protegida
const usersResponse = await fetch("http://localhost:8000/users/", {
  headers: { "Authorization": `Bearer ${access_token}` }
});

const users = await usersResponse.json();
console.log(users);
```

---

## ⚙️ Características de Seguridad

✅ **Tokens JWT con expiración:** 60 minutos
✅ **Hashing seguro de contraseñas:** bcrypt
✅ **Validación de credenciales:** Email + contraseña
✅ **Validación automática de token:** Middleware en endpoints protegidos
✅ **Variable de entorno para SECRET_KEY:** Cambiable en producción

---

## 📊 Usuarios de Prueba

Estos usuarios están precargados en la BD:

| Email | Contraseña | Rol |
|-------|-----------|-----|
| juan.admin@app.com | pass1 | Administrador |
| maria.nutri@app.com | pass2 | Nutricionista |
| carlos.c@gmail.com | pass3 | Paciente |
| ana.p@gmail.com | pass4 | Paciente |

> **Nota:** Las contraseñas están en texto plano en la BD como ejemplo. En producción deben estar hasheadas.

---

## 🔄 Flujo de Autenticación

```
┌─────────────────┐
│  Cliente        │
└────────┬────────┘
         │ 1. POST /auth/login (email, password)
         │
         ▼
┌──────────────────────────────────────┐
│  API FastAPI                         │
│  1. Verifica credenciales            │
│  2. Genera JWT Token                 │
└────────┬─────────────────────────────┘
         │ 2. Retorna Token
         │
         ▼
┌─────────────────┐
│  Cliente (Token)│
└────────┬────────┘
         │ 3. GET /users/ + header Authorization Header
         │
         ▼
┌──────────────────────────────────────┐
│  API FastAPI                         │
│  1. Valida Token                     │
│  2. Extrae datos del usuario         │
│  3. Ejecuta endpoint protegido       │
└────────┬─────────────────────────────┘
         │ 4. Retorna datos (200 OK)
         │
         ▼
┌─────────────────┐
│  Cliente        │
└─────────────────┘
```

---

## ❌ Errores Comunes

### Error: `401 Unauthorized - No se pudo validar el token`

**Causas:**
- Token no incluido en header
- Token expirado
- Token inválido o modificado

**Solución:** 
- Genera un nuevo token con `/auth/login`
- Asegúrate de incluir `Authorization: Bearer {token}` en el header

### Error: `401 Unauthorized - Credenciales inválidas`

**Causas:**
- Email no existe
- Contraseña incorrecta
- Usuario inactivo

**Solución:** 
- Verifica que el usuario exista y esté activo
- Comprueba que la contraseña sea correcta

---

## 📖 Documentación Interactiva

Accede a la documentación automática de FastAPI en Swagger:

```
http://localhost:8000/docs
```

Desde aquí puedes:
- Ver todos los endpoints
- Probar endpoints interactivamente
- Generar tokens de prueba
- Ejecutar solicitudes protegidas

---

## 🛠️ Próximos Pasos

1. **Cambiar SECRET_KEY en producción:** Usa una clave fuerte y única
2. **Hashear contraseñas existentes:** Update todos los usuarios con hash bcrypt
3. **Implementar refresh tokens:** Para mayor seguridad
4. **Agregar roles y permisos:** Validar acceso por rol

