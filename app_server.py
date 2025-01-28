

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
  st.link_button("Riscaldamento", "https://game.helaglobe.com/main/gameview/?game=633-d8cec02cd4de9dffc72cf3e43bfb4305")
with col2:
  st.link_button("Nuoto", "https://game.helaglobe.com/main/gameview/?game=632-f34a5b905a23b05f3a28323e613c44cb")
with col3:
  st.link_button("Ciclismo", "https://game.helaglobe.com/main/gameview/?game=630-f676683bfb26e0bfad25b6cc866c54ce")
with col4:
  st.link_button("Corsa", "https://game.helaglobe.com/main/gameview/?game=631-d13760f5d6cb31f1ef5c04ab169f61dd")
