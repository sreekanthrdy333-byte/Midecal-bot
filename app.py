import streamlit as st
import PIL.Image
import numpy as np
import cv2
from engine.llm import GeminiMedical
from engine.models import ModelRegistry, MockDetector
from utils.audio import text_to_speech, speech_to_text_ui
import os

st.set_page_config(page_title="MediAI Specialist Chatbot", page_icon="Hospital", layout="wide", initial_sidebar_state="expanded")

with open("styles/main.css") as f:
          st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
      if "current_image" not in st.session_state: st.session_state.current_image = None
            if "detection_results" not in st.session_state: st.session_state.detection_results = None
                  if "language" not in st.session_state: st.session_state.language = "English"

gemini = GeminiMedical()
registry = ModelRegistry()
mock_detector = MockDetector(gemini)

with st.sidebar:
          st.markdown("<h1>MediAI</h1>", unsafe_allow_html=True)
          st.markdown("### Multi-Super-Specialist AI")
          st.session_state.language = st.selectbox("Choose Language", ["English", "Spanish", "French", "Telugu", "Hindi"])
          st.divider()
          st.markdown("### Settings")
          auto_tts = st.toggle("Auto-Read Responses", value=True)
          st.divider()
          st.markdown("### Diagnostic Domains")
          st.info("Eye Disease\n\nLung Cancer\n\nBone Fracture\n\nPlant Health")

st.markdown("# Multi-Specialist Diagnostic Center")
st.markdown("#### *AI-Driven Insights for Health & Agriculture*")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
          st.markdown("### Image Analysis")
          uploaded_file = st.file_uploader("Upload Medical Scan (X-ray, MRI, Fundus, etc.)", type=["jpg", "jpeg", "png"])
          if uploaded_file:
                        image = PIL.Image.open(uploaded_file)
                        st.session_state.current_image = image
                        st.image(image, caption="Uploaded Image", use_container_width=True)
                        if st.button("Analyze Scan"):
                                          with st.spinner("Classifying & Routing..."):
                                                                category = gemini.classify_image_type(image)
                                                                st.success(f"Routed to Specialist: **{category}**")
                                                                img, detections = registry.detect(category, np.array(image))
                                                                if not detections:
                                                                                          detections = mock_detector.simulate_detection(category, image)
                                                                                      st.session_state.detection_results = detections
                                                                if detections:
                                                                                          st.markdown("### Detection Results")
                                                                                          for d in detections:
                                                                                                                        st.markdown(f'<div class="detection-card"><span class="status-badge status-danger">Detected: {d["label"]}</span> Confidence: {d["confidence"]:.2f}</div>', unsafe_allow_html=True)
                                                                                                                insights = gemini.get_medical_insights(detections, context_image=image)
                                                                                      st.session_state.messages.append({"role": "assistant", "content": insights})
                                                                if auto_tts: text_to_speech(insights[:300])

                                                with col2:
                                  st.markdown("### AI Specialist Consultation")
                                                          chat_container = st.container(height=500)
                                                          for message in st.session_state.messages:
                                                                        with chat_container.chat_message(message["role"]):
                                                                                          st.markdown(message["content"])

                                                                    if prompt := st.chat_input("Ask about symptoms, reports, or advice..."):
                                                                                  st.session_state.messages.append({"role": "user", "content": prompt})
                                                                                  with chat_container.chat_message("user"):
                                                                                                    st.markdown(prompt)
                                                                                                with chat_container.chat_message("assistant"):
                                                                                                                  with st.spinner("Consulting..."):
                                                                                                                                        response = gemini.chat_response(prompt, history=st.session_state.messages)
                                                                                                                                        st.markdown(response)
                                                                                                                                        st.session_state.messages.append({"role": "assistant", "content": response})
                                                                                                                                        if auto_tts: text_to_speech(response[:300])
                                                                                                                                              
                                                                                                                            st.markdown("---")
                                                                                                          st.markdown("#### Voice Input")
                                                                              voice_text = speech_to_text_ui()
                                                          if voice_text: st.info(f"Recognized: {voice_text}")
                                                                
