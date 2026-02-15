from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Ajustamos la importación para que funcione desde la carpeta 'app'
from .routes.user_routes import router as user_router
from .utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .controllers.user_controller import UserController
from .utils.auth import LoginRequest, TokenResponse
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

@app.post("/auth/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    """
    Endpoint de login que autentica al usuario y retorna un token JWT.
    
    **Parámetros:**
    - email: Email del usuario
    - password: Contraseña del usuario
    
    **Retorna:**
    - access_token: Token JWT válido por 60 minutos
    - token_type: "bearer"
    - user_id: ID del usuario autenticado
    - email: Email del usuario
    """
    user = user_controller.authenticate_user(credentials.email, credentials.password)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user["id"],
        "email": user["email"]
    }

# Vercel no ejecuta el bloque __main__, usa su propio servidor (uvicorn)
# pero lo dejamos para que sigas pudiendo ejecutarlo localmente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)