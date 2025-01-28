

import streamlit as st
import time
import firebase_admin
from firebase_admin import credentials, db

# Funzione HTML per pulsanti personalizzati
def custom_button(label, key):
    button_html = f"""
    <form action="" method="POST">
        <button type="submit" style="
            font-size: 24px;
            font-weight: bold;
            color: white;
            background-color: #007BFF;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            text-align: center;
        ">{label}</button>
    </form>
    """
    submitted = st.markdown(button_html, unsafe_allow_html=True)
    return submitted

# Aggiungi stile CSS per personalizzare i pulsanti
st.markdown("""
    <style>
    button[data-testid="stButton"] {
        font-size: 40px;
        font-weight: bold;
        color: white;
        background-color: #ff4b4b;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    button[data-testid="stButton"]:hover {
        background-color: #ff1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

st.image("logo.jpg",width=400)

col1, col2,col3, col4 = st.columns([1,1,1,1])
with col1:
  st.write("")
  st.write("")
  st.write("")
  st.write("")
  st.link_button("Riscaldamento", "https://game.helaglobe.com/main/gameview/?game=634-a56cc3d28c8361f192995fe925fc7f92",disabled=True)
with col2:
  st.write("")
  st.write("")
  st.write("")
  st.write("")
  st.link_button("Nuoto", "https://game.helaglobe.com/main/gameview/?game=635-f0ce36416abefe671629ae5bcf31d1b2",disabled=True)
with col3:
  st.write("")
  st.write("")
  st.write("")
  st.write("")
  st.link_button("Ciclismo", "https://game.helaglobe.com/main/gameview/?game=639-1cebeab015b906a88198e4c50a3e3d65")
with col4:
  st.write("")
  st.write("")
  st.write("")
  st.write("")
  st.link_button("Corsa", "https://game.helaglobe.com/main/gameview/?game=638-79c7f99522da888c5e008006d2dd3680")
