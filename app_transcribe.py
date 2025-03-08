import streamlit as st
import openai
import tempfile
import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pydub import AudioSegment
from google.oauth2.service_account import Credentials

# Configura la tua chiave API OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# Configurazione Google Drive (sostituisci con le credenziali corrette)
from google.oauth2 import service_account
credentials = Credentials.from_service_account_info(st.secrets["gdrive_service_account"])
drive_service = build("drive", "v3", credentials=creds)

#SCOPES = ["https://www.googleapis.com/auth/drive.file"]
#SERVICE_ACCOUNT_FILE = "path-to-your-service-account.json"
#credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#drive_service = build("drive", "v3", credentials=credentials)

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

audio_file = st.file_uploader("Carica il tuo file audio", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_file_path = tmp_file.name
    
    st.audio(tmp_file_path, format="audio/wav")
    
    with st.spinner("Trascrizione in corso..."):
        transcript_text = transcribe_audio(tmp_file_path)
        st.success("Trascrizione completata!")
        st.text_area("Testo Trascritto", transcript_text, height=200)
        
        # Salvataggio su Google Drive
        txt_file_path = tmp_file_path.replace(".wav", ".txt")
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcript_text)
        
        drive_file_id = save_to_drive(txt_file_path, "trascrizione.txt")
        st.success(f"File salvato su Google Drive con ID: {drive_file_id}")
    
    os.remove(tmp_file_path)
