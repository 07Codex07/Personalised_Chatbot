import streamlit as st
import speech_recognition as sr
import requests
from gtts import gTTS
import os

# Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# -- Functions --
def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are Vinayak, a AI/ML enthusiast answering personal reflective questions. Be honest, growth-focused, and inspiring."},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(GROQ_API_URL, headers=headers, json=body)
    return res.json()['choices'][0]['message']['content']

def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Recording... Speak now.")
        audio = r.listen(source)
        st.success("✅ Recorded.")
        return audio

def recognize_audio(audio):
    r = sr.Recognizer()
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return None

def speak_response(text):
    tts = gTTS(text=text, lang='en')
    filename = "response.mp3"
    tts.save(filename)
    return filename

# Web UI
st.set_page_config(page_title="Vinayak Voicebot", page_icon="🎤")
st.title("🎤 Vinayak's Voice Chatbot")

if "audio" not in st.session_state:
    st.session_state.audio = None

col1, col2 = st.columns(2)

with col1:
    if st.button("🎙 Start Recording", key="start_button"):
        st.session_state.audio = record_voice()

with col2:
    if st.button("⏹ Stop & Process", key="stop_button"):
        if st.session_state.audio:
            query = recognize_audio(st.session_state.audio)  #  define here
            if query:
                st.success(f"🗣 You said: {query}")
                with st.spinner("🤖 Thinking..."):
                    response = ask_groq(query)
                st.markdown(f"🤖 **Vinayak-bot says:** {response}")

                # 🔊 Speak response
                audio_file = speak_response(response)

                with open(audio_file, 'rb') as f:
                    st.audio(f.read(), format='audio/mp3')

                os.remove(audio_file)
            else:
                st.error("❌ Could not understand the audio. Try again.")
        else:
            st.warning("⚠️ You haven't recorded anything yet.")
