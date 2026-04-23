from gtts import gTTS
import os
import streamlit as st
import base64
def text_to_speech(text):
      try:
                tts = gTTS(text=text, lang='en')
                tts.save("r.mp3")
                with open("r.mp3", "rb") as f:
                              b = base64.b64encode(f.read()).decode()
                              st.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b}" type="audio/mp3"></audio>', unsafe_allow_html=True)
                          os.remove("r.mp3")
            except: pass
              def speech_to_text_ui():
                    from streamlit_mic_recorder import mic_recorder
                    audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')
                    if audio: return "Analyize image"
                          return None
