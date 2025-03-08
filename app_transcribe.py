import streamlit as st
import openai
import numpy as np
import base64
import tempfile
import os
from pydub import AudioSegment
import streamlit.components.v1 as components

# 🔑 API Key di OpenAI (inseriscila qui o usa streamlit secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Titolo dell'app
st.title("🎙️ Trascrizione Vocale con Whisper in Streamlit")

# **JavaScript per la registrazione audio nel browser**
audio_recorder_script = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];
        
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        
        document.getElementById("startRecording").disabled = true;
        document.getElementById("stopRecording").disabled = false;
    });
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            const base64data = reader.result.split(',')[1];
            fetch("/record_audio", {
                method: "POST",
                body: JSON.stringify({ audio: base64data }),
                headers: { "Content-Type": "application/json" }
            }).then(response => response.json())
              .then(data => {
                  document.getElementById("transcription").innerText = data.transcription;
              });
        };
    };
    
    document.getElementById("startRecording").disabled = false;
    document.getElementById("stopRecording").disabled = true;
}
</script>
"""

# **Aggiungere i pulsanti di registrazione**
st.markdown('<button id="startRecording" onclick="startRecording()">🎤 Avvia Registrazione</button>', unsafe_allow_html=True)
st.markdown('<button id="stopRecording" onclick="stopRecording()" disabled>⏹️ Stop Registrazione</button>', unsafe_allow_html=True)

# **Aggiungere lo script JavaScript**
components.html(audio_recorder_script, height=0)

# **Area di testo per mostrare la trascrizione**
st.subheader("📝 Trascrizione:")
transcription_text = st.empty()  # Spazio vuoto in cui apparirà la trascrizione

# **Backend per elaborare l'audio**
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/record_audio", methods=["POST"])
def record_audio():
    try:
        data = request.get_json()
        audio_base64 = data["audio"]
        
        # Decodifica l'audio Base64 in un file WAV temporaneo
        audio_bytes = base64.b64decode(audio_base64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            audio_path = temp_audio_file.name
        
        # **Trascrizione con Whisper**
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
        # **Elimina il file temporaneo**
        os.remove(audio_path)
        
        return jsonify({"transcription": transcript["text"]})
    
    except Exception as e:
        return jsonify({"error": str(e)})

# **Eseguire Flask in background**
import threading
threading.Thread(target=lambda: app.run(port=5001, debug=False, use_reloader=False)).start()
