# Proyecto NutriScan (Microservicios)

Este repositorio contiene dos proyectos desplegados en Vercel:

1. **API Principal (Python - FastAPI):** Carpeta `/NutriScan`
   - URL: "https://proyecto-rc.vercel.app/docs#/"
   - ✅ Autenticación JWT implementada
   - ✅ Base de datos normalizada en PostgreSQL (9 tablas)
   - ✅ Documentación: Ver `JWT_AUTHENTICATION.md`

2. **Servicio de Ubicaciones (Node.js - Express):** Carpeta `/servicios`
   - URL: "https://proyecto-rc-jju7-mbe5fe4en-richcams-projects.vercel.app"
   - ✅ Autenticación JWT implementada (3 tablas)

---

## 🔐 Autenticación JWT

### FastAPI (API Principal)

Para usar los endpoints protegidos:

1. **Login** (Obtener token):
   ```bash
   POST /auth/login
   Content-Type: application/json
   
   {
     "email": "juan.admin@app.com",
     "password": "pass1"
   }
   ```

2. **Usar token** en solicitudes protegidas:
   ```bash
   GET /users/
   Authorization: Bearer {token_recibido}
   ```

Ver documentación completa en: `NutriScan/JWT_AUTHENTICATION.md`

### Express (Servicio de Ubicaciones)

El servicio de ubicaciones también cuenta con JWT para endpoints de escritura.

---

## 📦 Requisitos del Proyecto (COMPLETADOS)

### ✅ 1. API con FastAPI
- ✅ 1.1 BD PostgreSQL normalizada (9 tablas con PK, UNIQUE, estado, creado, actualizado)
- ✅ 1.2 API con endpoints para CRUD de usuarios
- ✅ 1.3 JWT con validación implementado
- ✅ 1.3 Despliegue en Vercel

### ✅ 2. API con Express
- ✅ 2.1 BD PostgreSQL auxiliar (3 tablas con PK, UNIQUE, estado, creado, actualizado)
- ✅ 2.2 API con endpoints (GET/POST ubicaciones)
- ✅ 2.3 JWT con validación implementado
- ✅ 2.3 Despliegue en Vercel

