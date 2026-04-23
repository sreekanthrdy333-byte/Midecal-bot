import google.generativeai as genai
import PIL.Image
from config import GEMINI_API_KEY
class GeminiMedical:
      def __init__(self):
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.vision_model = genai.GenerativeModel('gemini-1.5-flash')
            def get_medical_insights(self, detections, context_image=None):
                      prompt = f"Medical AI findings: {detections}. Provide: Causes, Advice, Professional Consultation check."
                      if context_image: response = self.vision_model.generate_content([prompt, context_image])
else: response = self.model.generate_content(prompt)
        return response.text
    def chat_response(self, query, history=[]):
              chat = self.model.start_chat(history=history)
              return chat.send_message(query).text
          def classify_image_type(self, image):
                    prompt = "Classify: Chest X-ray, Eye Fundus, Bone X-ray, Plant Leaf, Other. Return ONLY name."
                    return self.vision_model.generate_content([prompt, image]).text.strip()
            
