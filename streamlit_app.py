import streamlit as st
import speech_recognition as sr
import threading
import wave
import pyaudio
import os
from io import BytesIO

# Initialize global variables
recording = False
paused = False
frames = []
recorder = None
transcription = ""

def start_recording():
    global recording, frames, paused, recorder
    recording = True
    paused = False
    frames = []
    recorder = pyaudio.PyAudio()

    stream = recorder.open(format=pyaudio.paInt16, 
                            channels=1, 
                            rate=44100, 
                            input=True, 
                            frames_per_buffer=1024)

    def record():
        global frames, recording, paused
        while recording:
            if not paused:
                data = stream.read(1024)
                frames.append(data)

        stream.stop_stream()
        stream.close()

    threading.Thread(target=record).start()

def stop_recording():
    global recording, recorder
    recording = False
    if recorder:
        recorder.terminate()
        recorder = None

def save_audio():
    output_file = BytesIO()
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
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
        paused = True

with col3:
    if st.button("Riprendi"):
        paused = False

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
