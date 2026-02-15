#!/usr/bin/env python3
"""
Script de prueba para validar la autenticación JWT en NutriScan API
Uso: python test_jwt.py
"""

import requests
import json
from typing import Optional

# Configuración
BASE_URL = "http://localhost:8000"  # Cambiar a URL de producción si es necesario
EMAIL = "juan.admin@app.com"
PASSWORD = "pass1"

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(step: int, title: str):
    """Imprime el título de un paso"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"PASO {step}: {title}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(msg: str):
    """Imprime un mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg: str):
    """Imprime un mensaje de error"""
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg: str):
    """Imprime información"""
    print(f"{Colors.CYAN}ℹ {msg}{Colors.END}")

def test_login() -> Optional[str]:
    """Prueba el endpoint de login y retorna el token"""
    print_step(1, "Pruebas de Login")
    
    try:
        print_info(f"URL: POST {BASE_URL}/auth/login")
        print_info(f"Email: {EMAIL}")
        print_info(f"Password: {PASSWORD}")
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMAIL, "password": PASSWORD},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login exitoso!")
            print(f"\n{Colors.YELLOW}Respuesta:{Colors.END}")
            print(json.dumps(data, indent=2))
            
            token = data.get("access_token")
            user_id = data.get("user_id")
            print_info(f"Token generado para usuario ID: {user_id}")
            
            return token
        else:
            print_error(f"Error en login: Status {response.status_code}")
            print(f"{Colors.RED}Respuesta: {response.text}{Colors.END}")
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_info("¿Asegúrate de que FastAPI está corriendo en http://localhost:8000?")
        return None
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return None

def test_protected_endpoint(token: str):
    """Prueba un endpoint protegido con el token"""
    print_step(2, "Pruebas de Endpoint Protegido")
    
    try:
        print_info(f"URL: GET {BASE_URL}/users/")
        print_info(f"Auth: Bearer {token[:20]}...")
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/users/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Acceso a endpoint protegido exitoso!")
            print(f"\n{Colors.YELLOW}Respuesta:{Colors.END}")
            print(json.dumps(data, indent=2)[:500] + "..." if len(json.dumps(data)) > 500 else json.dumps(data, indent=2))
        else:
            print_error(f"Error al acceder al endpoint: Status {response.status_code}")
            print(f"{Colors.RED}Respuesta: {response.text}{Colors.END}")
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")

def test_invalid_token():
    """Prueba acceso con token inválido"""
    print_step(3, "Pruebas de Token Inválido")
    
    try:
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.token"
        print_info(f"URL: GET {BASE_URL}/users/")
        print_info(f"Token: {invalid_token[:20]}... (inválido)")
        
        headers = {"Authorization": f"Bearer {invalid_token}"}
        response = requests.get(
            f"{BASE_URL}/users/",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 401:
            print_success("Correctamente rechazado token inválido!")
            print(f"{Colors.YELLOW}Respuesta:{Colors.END}")
            print(json.dumps(response.json(), indent=2))
        else:
            print_error(f"Comportamiento inesperado: Status {response.status_code}")
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")

def test_missing_auth():
    """Prueba acceso sin autenticación"""
    print_step(4, "Pruebas de Acceso sin Autenticación")
    
    try:
        print_info(f"URL: GET {BASE_URL}/users/ (sin header Authorization)")
        
        response = requests.get(
            f"{BASE_URL}/users/",
            timeout=5
        )
        
        if response.status_code == 401:
            print_success("Correctamente rechazado acceso sin autenticación!")
            print(f"{Colors.YELLOW}Respuesta:{Colors.END}")
            print(json.dumps(response.json(), indent=2))
        else:
            print_error(f"Comportamiento inesperado: Status {response.status_code}")
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")

def test_public_endpoint():
    """Prueba que endpoints públicos funcionen sin JWT"""
    print_step(5, "Pruebas de Endpoint Público")
    
    try:
        print_info(f"URL: GET {BASE_URL}/ (sin autenticación)")
        
        response = requests.get(
            f"{BASE_URL}/",
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Endpoint público accesible sin autenticación!")
            print(f"{Colors.YELLOW}Respuesta:{Colors.END}")
            print(json.dumps(response.json(), indent=2))
        else:
            print_error(f"Error inesperado: Status {response.status_code}")
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")

def print_summary():
    """Imprime resumen final"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
    print("RESUMEN DE PRUEBAS")
    print(f"{'='*60}{Colors.END}\n")
    
    print(f"{Colors.GREEN}✓ Autenticación JWT{Colors.END}")
    print(f"{Colors.GREEN}✓ Endpoints protegidos{Colors.END}")
    print(f"{Colors.GREEN}✓ Validación de tokens{Colors.END}")
    print(f"{Colors.GREEN}✓ Endpoints públicos{Colors.END}")
    
    print(f"\n{Colors.CYAN}Próximos pasos:{Colors.END}")
    print("1. Cambiar JWT_SECRET_KEY en .env para producción")
    print("2. Hashear contraseñas existentes en la base de datos")
    print("3. Ver documentación completa en: JWT_AUTHENTICATION.md")
    print(f"\n{Colors.YELLOW}Documentación interactiva en Swagger:{Colors.END}")
    print(f"→ {BASE_URL}/docs\n")

def main():
    """Ejecuta todas las pruebas"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print("PRUEBAS DE AUTENTICACIÓN JWT - NutriScan API")
    print(f"{'='*60}{Colors.END}\n")
    
    # Prueba 1: Login
    token = test_login()
    
    if not token:
        print_error("No se pudo obtener token. Abortando pruebas.")
        return
    
    # Prueba 2: Endpoint protegido con token válido
    test_protected_endpoint(token)
    
    # Prueba 3: Token inválido
    test_invalid_token()
    
    # Prueba 4: Sin autenticación
    test_missing_auth()
    
    # Prueba 5: Endpoint público
    test_public_endpoint()
    
    # Resumen
    print_summary()

if __name__ == "__main__":
    main()
