from ultralytics import YOLO
import cv2
import numpy as np
class ModelRegistry:
      def __init__(self):
                self.models = {"Chest X-ray": "yolov8n.pt", "Eye Fundus": "yolov8n.pt", "Bone X-ray": "yolov8n.pt", "Plant Leaf": "yolov8n.pt"}
                self.loaded = {}
            def detect(self, cat, img):
                      if cat not in self.models: return None, []
                                if cat not in self.loaded: self.loaded[cat] = YOLO(self.models[cat])
                                          res = self.loaded[cat](img)
        dets = [{"class": self.loaded[cat].names[int(b.cls)], "confidence": float(b.conf), "bbox": [float(x) for x in b.xyxy[0]]} for b in res[0].boxes]
        return res[0].plot(), dets
class MockDetector:
      def __init__(self, g): self.g = g
            def simulate_detection(self, cat, img):
                      return [{"class": "Condition", "confidence": 0.89, "bbox": [50, 50, 200, 200]}]
