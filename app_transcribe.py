import streamlit as st
import openai
import tempfile
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import numpy as np
from pydub import AudioSegment
import queue

# Configura la tua chiave API OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# Configurazione Google Drive
creds = Credentials.from_service_account_info(st.secrets["gdrive_service_account"])
drive_service = build("drive", "v3", credentials=creds)

def save_to_drive(file_path, file_name):
    file_metadata = {"name": file_name, "mimeType": "text/plain"}
    media = MediaFileUpload(file_path, mimetype="text/plain")
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

st.title("🎙️ Registrazione Audio e Trascrizione in Tempo Reale")

# Configurazione WebRTC per la registrazione audio
RTC_CONFIGURATION = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
audio_queue = queue.Queue()

def audio_callback(frame: av.AudioFrame):
    audio = frame.to_ndarray()
    audio_queue.put(audio)
    return frame

webrtc_ctx = webrtc_streamer(
    key="audio_recorder",
    mode=WebRtcMode.SENDONLY,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
    audio_processor_factory=lambda: audio_callback
)

if st.button("Interrompi e Trascrivi"):  
    if not audio_queue.empty():
        st.spinner("Elaborazione dell'audio...")
        audio_data = []
        while not audio_queue.empty():
            audio_data.append(audio_queue.get())
        
        audio_data = np.concatenate(audio_data, axis=0)
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        audio_segment = AudioSegment(
            audio_data.tobytes(), frame_rate=48000, sample_width=2, channels=1
        )
        temp_audio_file_path = temp_audio_file.name
        audio_segment.export(temp_audio_file_path, format="wav")
        
        transcript_text = transcribe_audio(temp_audio_file_path)
        st.success("Trascrizione completata!")
        st.text_area("Testo Trascritto", transcript_text, height=200)
        
        # Salvataggio su Google Drive
        txt_file_path = temp_audio_file_path.replace(".wav", ".txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcript_text)
        
        drive_file_id = save_to_drive(txt_file_path, "trascrizione.txt")
        st.success(f"File salvato su Google Drive con ID: {drive_file_id}")
        
        os.remove(temp_audio_file_path)
