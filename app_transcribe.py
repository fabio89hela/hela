import streamlit as st
import openai
import numpy as np
import base64
import tempfile
import os
import streamlit.components.v1 as components

# 🔑 Imposta la tua API Key di OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎙️ Trascrizione Vocale con Whisper")

# **Componenti HTML e JavaScript per registrare audio**
audio_recorder_script = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registratore</title>
</head>
<body>

<button onclick="startRecording()" id="startBtn">🎤 Avvia Registrazione</button>
<button onclick="stopRecording()" id="stopBtn" disabled>⏹️ Stop Registrazione</button>
<textarea id="audioData" style="display:none;"></textarea>

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
        
        document.getElementById("startBtn").disabled = true;
        document.getElementById("stopBtn").disabled = false;
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
            window.parent.postMessage(base64data, "*");
        };
    };

    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;
}
</script>
</body>
</html>
"""

# **Mostra il registratore in un iFrame**
components.html(audio_recorder_script, height=150)

# **Ricezione dell'audio**
audio_data = st.text_area("📥 Dati Audio (Base64)", "", height=100)

# **Elaborazione dell’audio quando viene ricevuto**
if audio_data:
    st.success("🎙️ Audio ricevuto! Trascrizione in corso...")

    # Convertire base64 in file WAV
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
