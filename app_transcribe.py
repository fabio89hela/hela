import streamlit as st
import openai
import numpy as np
import base64
import tempfile
import os
from pydub import AudioSegment

# Imposta la tua API Key di OpenAI
openai.api_key = "YOUR_OPENAI_API_KEY"

# Titolo dell'app
st.title("🎙️ Trascrizione vocale in tempo reale con Whisper")

# JavaScript per la registrazione dell'audio nel browser
audio_recorder_script = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
    });
}

function stopRecording() {
    return new Promise(resolve => {
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64data = reader.result.split(',')[1];
                resolve(base64data);
            };
        };
        mediaRecorder.stop();
    });
}

let startBtn = document.getElementById("startRecording");
let stopBtn = document.getElementById("stopRecording");

startBtn.onclick = () => {
    audioChunks = [];
    startRecording();
    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = async () => {
    stopBtn.disabled = true;
    startBtn.disabled = false;
    const audioBase64 = await stopRecording();
    window.parent.postMessage(audioBase64, "*");
};
</script>
"""

# Pulsanti per controllare la registrazione
st.markdown('<button id="startRecording">🎤 Avvia Registrazione</button>', unsafe_allow_html=True)
st.markdown('<button id="stopRecording" disabled>⏹️ Stop Registrazione</button>', unsafe_allow_html=True)
st.components.v1.html(audio_recorder_script, height=0)

# **JavaScript per ricevere i dati audio**
audio_data = st_javascript("""
    return new Promise((resolve) => {
        window.addEventListener("message", (event) => {
            resolve(event.data);
        });
    });
""")

# **Verifica se abbiamo ricevuto l'audio**
if audio_data:
    st.success("🎙️ Audio ricevuto! Elaborazione in corso...")

    # Convertire l'audio base64 in file WAV
    audio_bytes = base64.b64decode(audio_data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        audio_path = temp_audio_file.name

    # **Mostra l'audio registrato**
    st.audio(audio_path, format="audio/wav")

    # **Usa Whisper per la trascrizione**
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # **Mostra la trascrizione**
    st.subheader("📝 Trascrizione")
    st.write(transcript["text"])

    # **Cancella il file temporaneo**
    os.remove(audio_path)
