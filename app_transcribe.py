from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av

def audio_callback(frame):
    audio = frame.to_ndarray()
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        try:
            text = recognizer.recognize_google(source)
            st.write(f"🗣️ {text}")
        except:
            st.write("🔴 Could not transcribe")
    return av.AudioFrame.from_ndarray(audio)

st.title("🎤 Live Speech to Text")
webrtc_streamer(key="speech", mode=WebRtcMode.SENDRECV, audio_receiver_size=1024, video_frame_callback=None, audio_frame_callback=audio_callback)
