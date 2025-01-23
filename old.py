import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# Inizializza Firebase utilizzando i secrets di Streamlit
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://aiom---torino-default-rtdb.europe-west1.firebasedatabase.app/'
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

# Funzione per recuperare lo stato del timer
def get_timer_data():
    timer_data = timer_ref.get()
    if timer_data is None:
        timer_data = {"start_time": None, "duration": 0, "running": False}
    return timer_data

# Layout dell'app
st.title("Timer Condiviso")

# Recupera lo stato del timer
timer_data = get_timer_data()

# Se il timer non è attivo, mostra l'opzione per avviarlo
if not timer_data["running"]:
    duration_minutes = st.number_input("Durata del timer (in minuti):", min_value=1, max_value=60, value=5)
    if st.button("Avvia Timer", key="start_button"):
        start_timer(duration_minutes * 60)

# Placeholder per il timer attivo
placeholder = st.empty()

# Pulsante "Ferma Timer" fuori dal ciclo
stop_pressed = False
if timer_data["running"]:
    stop_pressed = st.button("Ferma Timer", key="stop_button")

# Timer in esecuzione
if timer_data["running"]:
    while True:
        timer_data = get_timer_data()
        if not timer_data["running"]:
            placeholder.empty()
            st.info("Il timer è stato fermato.")
            break

        # Calcola il tempo rimanente
        elapsed_time = time.time() - timer_data["start_time"]
        remaining_time = max(0, timer_data["duration"] - elapsed_time)

        # Mostra il timer
        with placeholder.container():
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.subheader(f"Tempo rimanente: {minutes:02d}:{seconds:02d}")

        # Se il pulsante è stato premuto, ferma il timer
        if stop_pressed:
            stop_timer()
            placeholder.empty()
            st.info("Il timer è stato fermato.")
            break

        # Quando il timer scade
        if remaining_time <= 0:
            st.success("Il timer è scaduto!")
            stop_timer()
            placeholder.empty()
            break

        # Aggiorna la pagina ogni secondo
        time.sleep(1)

# Mostra messaggio di default quando il timer non è attivo
if not timer_data["running"]:
    st.info("Il timer non è attivo. Puoi avviarne uno nuovo.")
