import streamlit as st
import openai
import base64
import tempfile
import os
import time
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript

# 🔑 Inserisci la tua API Key di OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎙️ Trascrizione Vocale con Whisper")

# **JavaScript per la registrazione audio nel browser e salvataggio in `localStorage`**
audio_recorder_script = """
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
            localStorage.setItem("audio_base64", base64data);
            localStorage.setItem("audio_timestamp", Date.now()); // Aggiorna timestamp
            document.getElementById("status").innerText = "✅ Audio salvato!";
        };
    };

    document.getElementById("startBtn").disabled = false;
    document.getElementById("stopBtn").disabled = true;
}
</script>

<button onclick="startRecording()" id="startBtn">🎤 Avvia Registrazione</button>
<button onclick="stopRecording()" id="stopBtn" disabled>⏹️ Stop Registrazione</button>
<p id="status">⏳ Pronto a registrare...</p>
"""

# **Mostra il registratore in Streamlit**
components.html(audio_recorder_script, height=300)

# **Funzione per leggere `localStorage` in Streamlit**
def get_javascript_value(js_code, key):
    """Esegue un comando JavaScript e ottiene il valore di ritorno"""
    components.html(
        f"""
        <script>
        var value = {js_code};
        var streamlitTextArea = parent.document.querySelector('textarea');
        streamlitTextArea.value = value;
        streamlitTextArea.dispatchEvent(new Event("input", {{ bubbles: true }}));
        </script>
        """,
        height=0,
    )
    return st.text_area("📥 Dati Audio (Base64)", key=key, height=100)

# **Controlliamo continuamente se `localStorage` è stato aggiornato**
prev_timestamp = st.session_state.get("prev_timestamp", 0)

i=0
while True:
    i=1
    timestamp = get_javascript_value("localStorage.getItem('audio_timestamp');", "audio_timestamp"+str(i))
    if timestamp and timestamp.isnumeric() and int(timestamp) > prev_timestamp:
        # **Se il timestamp è aggiornato, leggiamo l'audio Base64**
        audio_data = get_javascript_value("localStorage.getItem('audio_base64');", "audio_base64"+str(i))
        st.session_state["prev_timestamp"] = int(timestamp)
        break
    time.sleep(1)

# **Se abbiamo ricevuto l'audio, procediamo alla trascrizione**
if "audio_base64" in st.session_state:
    audio_data = st.session_state["audio_base64"]
    st.success("🎙️ Audio ricevuto! Trascrizione in corso...")

    # **Salviamo l'audio in un file temporaneo**
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
