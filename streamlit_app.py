import streamlit as st
import sounddevice as sd
import numpy as np
import wave
from io import BytesIO
import speech_recognition as sr

# Initialize global variables
recording = False
frames = []
transcription = ""

def start_recording():
    global recording, frames
    recording = True
    frames = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        frames.append(indata.copy())

    sd.InputStream(callback=callback, channels=1, samplerate=44100, dtype='int16').start()

def stop_recording():
    global recording
    recording = False
    sd.stop()

def save_audio():
    output_file = BytesIO()
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 2 bytes per sample
    wf.setframerate(44100)
    wf.writeframes(b''.join([frame.tobytes() for frame in frames]))
    wf.close()
    output_file.seek(0)
    return output_file

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Unable to transcribe audio."
        except sr.RequestError:
            return "API request error."

# Streamlit app
st.title("Registratore e Trascrittore Audio")

if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# Buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Avvia Registrazione"):
        start_recording()

with col2:
    if st.button("Pausa"):
        recording = False

with col3:
    if st.button("Riprendi"):
        start_recording()

with col4:
    if st.button("Ferma e Salva"):
        stop_recording()
        audio_file = save_audio()
        transcription = transcribe_audio(audio_file)
        st.session_state.transcription = transcription
        st.audio(audio_file, format='audio/wav')

# Show transcription
st.text_area("Trascrizione automatica (modificabile):", 
             value=st.session_state.transcription, 
             height=200, 
             on_change=lambda: setattr(st.session_state, 'transcription', st.session_state.transcription))

# Download button
if not recording and len(frames) > 0:
    audio_file = save_audio()
    st.download_button("Scarica Audio", 
                       data=audio_file, 
                       file_name="registrazione.wav", 
                       mime="audio/wav")
