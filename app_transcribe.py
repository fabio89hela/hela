import streamlit as st
import openai
import numpy as np
import base64
import tempfile
import os
from pydub import AudioSegment
import streamlit.components.v1 as components

# 🔑 API Key di OpenAI (inseriscila qui o usa secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎙️ Trascrizione vocale con Whisper")

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
            document.getElementById("audioData").value = base64data;
        };
    };
    
    document.getElementById("startRecording").disabled = false;
    document.getElementById("stopRecording").disabled = true;
}
</script>
"""

# **Pulsanti di registrazione**
st.markdown('<button id="startRecording" onclick="startRecording()">🎤 Avvia Registrazione</button>', unsafe_allow_html=True)
st.markdown('<button id="stopRecording" onclick="stopRecording()" disabled>⏹️ Stop Registrazione</button>', unsafe_allow_html=True)

# **Campo nascosto per ricevere l’audio**
audio_data = st.text_area("📥 Dati Audio (Base64)", "", height=100)

# **Aggiungere il codice JavaScript**
components.html(audio_recorder_script, height=0)

# **Elaborazione dell’audio quando viene ricevuto**
if audio_data:
    st.success("🎙️ Audio ricevuto! Trascrizione in corso...")

    # Convertire base64 in file WAV temporaneo
    audio_bytes = base64.b64decode(audio_data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        audio_path = temp_audio_file.name

    # **Mostrare l’audio registrato**
    st.audio(audio_path, format="audio/wav")

    # **Trascrivere con Whisper**
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # **Mostrare la trascrizione**
    st.subheader("📝 Trascrizione:")
    st.write(transcript["text"])

    # **Eliminare il file temporaneo**
    os.remove(audio_path)
