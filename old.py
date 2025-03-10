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

# Layout dell'app
st.title("Timer Condiviso")

# Ottieni stato attuale del timer dal database
timer_data = timer_ref.get()
if not timer_data:
    # Inizializza i dati nel caso in cui siano assenti
    timer_data = {"start_time": None, "duration": 0, "running": False}

# Assicurati che le chiavi esistano nel dizionario
running = timer_data.get("running", False)
start_time = timer_data.get("start_time", None)
duration = timer_data.get("duration", 0)

# Input iniziale per impostare il timer (una sola volta)
if "timer_initialized" not in st.session_state:
    st.session_state.timer_initialized = False

if not st.session_state.timer_initialized:
    duration_minutes = st.number_input("Durata del timer (in minuti):", min_value=1, max_value=60, value=5)
    if st.button("Avvia Timer"):
        start_timer(duration_minutes * 60)
        st.session_state.timer_initialized = True

# Aggiorna dinamicamente la schermata
placeholder = st.empty()
while True:
    # Contenuto dinamico
    with placeholder.container():
        if running:
            # Calcola tempo rimanente
            elapsed_time = time.time() - start_time
            remaining_time = max(0, duration - elapsed_time)

            # Mostra il timer
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            st.subheader(f"Tempo rimanente: {minutes:02d}:{seconds:02d}")

            # Fermare il timer
            if st.button("Ferma Timer", key="stop_button"):
                stop_timer()
                st.session_state.timer_initialized = False

            # Mostra messaggio quando scade
            if remaining_time <= 0:
                st.success("Il timer è scaduto!")
                stop_timer()
                st.session_state.timer_initialized = False

        else:
            st.info("Il timer non è attivo. Puoi avviarne uno nuovo.")
            st.session_state.timer_initialized = False

    # Ottieni nuovamente lo stato del timer dal database
    timer_data = timer_ref.get()
    if not timer_data:
        timer_data = {"start_time": None, "duration": 0, "running": False}

    running = timer_data.get("running", False)
    start_time = timer_data.get("start_time", None)
    duration = timer_data.get("duration", 0)

    # Aspetta 1 secondo prima di aggiornare
    time.sleep(1)
    st.rerun()
