import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import av
import speech_recognition as sr
import queue

# Set page title
st.set_page_config(page_title="Live Speech to Text", page_icon="🎙️")

# Streamlit UI
st.title("🎙️ Live Speech-to-Text Transcription")
st.write("Speak into your microphone, and your words will be transcribed in real-time.")

# Queue for storing audio frames
audio_queue = queue.Queue()
recognizer = sr.Recognizer()

# WebRTC Configuration (uses Google's public STUN servers)
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

def audio_callback(frame: av.AudioFrame):
    """ Process incoming audio frames """
    audio = frame.to_ndarray()
    audio_queue.put(audio)
    return frame

def recognize_audio():
    """ Continuously transcribe audio from the queue """
    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            with sr.AudioFile(audio_data) as source:
                try:
                    text = recognizer.recognize_google(source)
                    st.session_state["transcription"] += text + " "
                except sr.UnknownValueError:
                    st.session_state["transcription"] += "[Unclear speech] "
                except sr.RequestError:
                    st.session_state["transcription"] += "[Speech service unavailable] "

# Initialize session state for transcription
if "transcription" not in st.session_state:
    st.session_state["transcription"] = ""

# WebRTC streamer for real-time audio
webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": False, "audio": True},
    audio_frame_callback=audio_callback,
)

# Display real-time transcription
st.subheader("📝 Live Transcription:")
st.write(st.session_state["transcription"])

# Reset transcription
if st.button("Clear Transcription"):
    st.session_state["transcription"] = ""
