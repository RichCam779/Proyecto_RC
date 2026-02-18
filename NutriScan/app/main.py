from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .routes.user_routes import router as user_router
from .utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SimpleTokenResponse
from .controllers.user_controller import UserController
from .utils.auth import LoginRequest
from datetime import timedelta

# Configuración de la API
app = FastAPI(title="NutriScan API")

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de usuario
app.include_router(user_router)

# Controlador de usuarios
user_controller = UserController()

@app.get("/")
def home():
    return {
        "message": "NutriScan API está en línea",
        "docs": "/docs"
    }

# Endpoint de login
@app.post("/login", response_model=SimpleTokenResponse)
def login(credentials: LoginRequest):
    user = user_controller.authenticate_user(credentials.email, credentials.password)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access": access_token
    }

# Configuración de Swagger
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

# Iniciar servidor
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
