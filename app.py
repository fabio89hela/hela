import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import datetime
import time

# Inizializza Firebase
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

# Riferimento al database Firebase
timer_ref = db.reference("timer")

# Funzione per ottenere lo stato attuale del timer
def get_timer_state():
    state = timer_ref.get()
    if state is None:
        return {"running": False, "start_time": None, "elapsed": 0}
    return state

# Funzione per aggiornare lo stato del timer
def update_timer_state(state):
    timer_ref.set(state)

# Interfaccia Streamlit
st.title("Timer Sincronizzato con Firebase")

# Ottieni lo stato attuale del timer
timer_state = get_timer_state()

# Calcola il tempo trascorso
if timer_state["running"]:
    start_time = datetime.datetime.fromisoformat(timer_state["start_time"])
    elapsed_time = (datetime.datetime.now() - start_time).total_seconds() + timer_state["elapsed"]
else:
    elapsed_time = timer_state["elapsed"]

# Mostra il timer
elapsed_time_display = str(datetime.timedelta(seconds=int(elapsed_time)))
st.header(f"Tempo Trascorso: {elapsed_time_display}")

# Pulsanti per avviare o fermare il timer
col1, col2 = st.columns(2)

with col1:
    if st.button("Avvia"):
        if not timer_state["running"]:
            timer_state["running"] = True
            timer_state["start_time"] = datetime.datetime.now().isoformat()
            update_timer_state(timer_state)

with col2:
    if st.button("Ferma"):
        if timer_state["running"]:
            start_time = datetime.datetime.fromisoformat(timer_state["start_time"])
            timer_state["elapsed"] += (datetime.datetime.now() - start_time).total_seconds()
            timer_state["running"] = False
            timer_state["start_time"] = None
            update_timer_state(timer_state)

# Pulsante per azzerare il timer
if st.button("Reset"):
    timer_state = {"running": False, "start_time": None, "elapsed": 0}
    update_timer_state(timer_state)

# Aggiornamento live del timer se in esecuzione
if timer_state["running"]:
    time.sleep(1)
    st.experimental_rerun()
