import os
import sys

# Añadir el directorio NutriScan al path para poder importar app.utils.ai_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "NutriScan")))

try:
    from app.utils.ai_utils import YOLOHandler
    import onnxruntime as ort
    print("Importación exitosa.")
except ImportError as e:
    print(f"Error de importación: {e}")
    sys.exit(1)

def test_model_init():
    print("\n--- Probando inicialización de YOLOHandler ---")
    # En local (Windows), usaremos un nombre de modelo temporal para no ensuciar /tmp si existe algo parecido
    # Pero simularemos la lógica de Vercel
    handler = YOLOHandler(model_name="test_yolov8n.onnx")
    
    print(f"Ruta del modelo: {handler.model_path}")
    if handler.session:
        print("ÉXITO: Sesión de ONNX Runtime cargada.")
    else:
        print("AVISO: Sesión no cargada (esperado si falla la descarga o falta entorno).")
        print("Verificando si el modo degradado funciona...")
        biotype, conf = handler.detect_and_analyze_biotype(b"fake_image_bytes")
        print(f"Resultado biotipo (degradado): {biotype}, Confianza: {conf}")
        if biotype == "Mesomorfo":
            print("ÉXITO: El modo degradado devolvió el resultado por defecto.")

if __name__ == "__main__":
    test_model_init()
