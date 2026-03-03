import cv2
import numpy as np
from ultralytics import YOLO
import os

class YOLOHandler:
    def __init__(self, model_path="yolov8n.pt"):
        # Esto descargará el modelo si no existe
        self.model = YOLO(model_path)
    
    def detect_and_analyze_biotype(self, image_bytes):
        # Convertir bytes a imagen de OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Ejecutar YOLO para detectar personas
        results = self.model(img, classes=[0]) # 0 es persona en COCO
        
        if len(results[0].boxes) == 0:
            return None, 0.0
            
        # Tomar la primera detección de persona
        box = results[0].boxes[0]
        conf = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0]
        
        # Calcular proporciones básicas para el biótipo (Simulación robusta)
        width = x2 - x1
        height = y2 - y1
        ratio = width / height
        
        # Lógica de biótipo basada en relación de aspecto (ratio)
        if ratio < 0.35:
            biotype = "Ectomorfo"
        elif ratio > 0.45:
            biotype = "Endomorfo"
        else:
            biotype = "Mesomorfo"
            
        return biotype, conf

    def detect_food(self, image_bytes):
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Clases de comida en COCO (yolov8n):
        # 46: banana, 47: apple, 48: sandwich, 49: orange, 50: broccoli, 
        # 51: carrot, 52: hot dog, 53: pizza, 54: donut, 55: cake
        food_classes = [46, 47, 48, 49, 50, 51, 52, 53, 54, 55]
        
        results = self.model(img, classes=food_classes)
        
        detections = []
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            label = self.model.names[class_id]
            conf = float(box.conf[0])
            detections.append({
                "label": label,
                "confidence": conf
            })
            
        return detections
