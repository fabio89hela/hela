import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# Configurazione Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/your-firebase-credentials.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://<your-database-name>.firebaseio.com/'
    })

# Configurazione della pagina
st.set_page_config(page_title="Timer Condiviso", layout="centered")

# Firebase Database Reference
timer_ref = db.reference("timer")

# Funzione per avviare il timer
def start_timer(duration):
    timer_ref.set({
        "start_time": time.time(),
        "duration": duration,
        "running": True
    })

# Funzione per fermare il timer
def stop_timer():
    timer_ref.update({
        "running": False
    })

# Ottieni stato attuale del timer dal database
timer_data = timer_ref.get()
if timer_data is None:
    timer_data = {"start_time": None, "duration": 0, "running": False}

# Layout dell'app
st.title("Timer Condiviso")

if not timer_data["running"]:
    # Input per impostare il timer
    duration_minutes = st.number_input("Durata del timer (in minuti):", min_value=1, max_value=60, value=5)
    if st.button("Avvia Timer"):
        start_timer(duration_minutes * 60)

if timer_data["running"]:
    # Calcola tempo rimanente
    elapsed_time = time.time() - timer_data["start_time"]
    remaining_time = max(0, timer_data["duration"] - elapsed_time)

    # Mostra il timer
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    st.subheader(f"Tempo rimanente: {minutes:02d}:{seconds:02d}")

    # Fermare il timer
    if st.button("Ferma Timer"):
        stop_timer()

    # Mostra messaggio quando scade
    if remaining_time <= 0:
        st.success("Il timer è scaduto!")
        stop_timer()

if not timer_data["running"]:
    st.info("Il timer non è attivo. Puoi avviarne uno nuovo.")
