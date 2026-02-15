from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
# Ajustamos la importación para que funcione desde la carpeta 'app'
from .routes.user_routes import router as user_router
from .utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SimpleTokenResponse
from .controllers.user_controller import UserController
from .utils.auth import LoginRequest
from datetime import timedelta

app = FastAPI(title="NutriScan API")

# Configuramos los orígenes para permitir tu entorno local y el futuro despliegue
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"  # Permite todos los orígenes temporalmente para facilitar el testeo en Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(user_router)

# Instancia del controlador
user_controller = UserController()

@app.get("/")
def home():
    return {
        "message": "NutriScan API está en línea",
        "docs": "/docs"
    }

@app.post("/login", response_model=SimpleTokenResponse)
def login(credentials: LoginRequest):
    """
    Endpoint de login que autentica al usuario y retorna un token JWT.
    
    **Parámetros:**
    - email: Email del usuario
    - password: Contraseña del usuario
    
    **Retorna:**
    - access: Token JWT válido por 60 minutos
    """
    user = user_controller.authenticate_user(credentials.email, credentials.password)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access": access_token
    }

# Configurar OpenAPI con seguridad Bearer para Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="NutriScan API",
        version="1.0.0",
        description="API de NutriScan con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Vercel no ejecuta el bloque __main__, usa su propio servidor (uvicorn)
# pero lo dejamos para que sigas pudiendo ejecutarlo localmente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)