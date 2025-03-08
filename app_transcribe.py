import streamlit as st
import openai
import numpy as np
import base64
import tempfile
import os
import streamlit.components.v1 as components

# 🔑 Inserisci la tua API Key di OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎙️ Trascrizione Vocale con Whisper")

# **JavaScript per la registrazione audio nel browser**
audio_recorder_script = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registratore Audio</title>
</head>
<body>

<button onclick="startRecording()" id="startBtn">🎤 Avvia Registrazione</button>
<button onclick="stopRecording()" id="stopBtn" disabled>⏹️ Stop Registrazione</button>
<p id="status">⏳ Pronto a registrare...</p>

<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        audioChunks = [];
        document.getElementById("status").innerText = "🔴 Registrazione in corso...";
        
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        
        document.getElementById("startBtn").disabled = true;
        document.getElementById("stopBtn").disabled = false;
    });
}

function stopRecording() {
    mediaRecorder.stop();
    document.getElementById("status").innerText = "⏳ Elaborazione audio...";

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            const base64data = reader.result.split(',')[1];
            window.parent.postMessage({ audio: base64data }, "*");
            document.getElementById("status").innerText = "✅ Audio inviato!";
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
components.html(audio_recorder_script, height=250)

# **Placeholder per ricevere i dati Base64**
audio_data = st.text_area("📥 Dati Audio (Base64)", "", height=100, key="audio_input")

# **JavaScript per ricevere i dati da `postMessage` e aggiornare Streamlit**
js_code = """
<script>
window.addEventListener("message", (event) => {
    if (event.data.audio) {
        const streamlitTextArea = parent.document.querySelector('textarea');
        streamlitTextArea.value = event.data.audio;
        streamlitTextArea.dispatchEvent(new Event("input", { bubbles: true }));
    }
});
</script>
"""

# **Esegue il codice JavaScript in Streamlit**
components.html(js_code, height=0)

# **Funzione per salvare il file audio ricevuto**
def save_audio_from_base64(audio_base64):
    audio_bytes = base64.b64decode(audio_base64)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        return temp_audio_file.name

# **Quando viene ricevuto l'audio, avvia la trascrizione**
if audio_data:
    st.success("🎙️ Audio ricevuto! Trascrizione in corso...")

    # **Salva l'audio in un file**
    audio_path = save_audio_from_base64(audio_data)

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
