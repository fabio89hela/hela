import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import time

# Inizializzazione Firebase
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

# Riferimento al nodo del database Firebase
timer_ref = db.reference('timer')

# Funzioni helper per Firebase
def update_timer(status, end_time=None):
    timer_ref.set({
        'status': status,
        'end_time': end_time.isoformat() if end_time else None,
        'last_updated': datetime.now().isoformat()
    })

def get_timer():
    data = timer_ref.get()
    if data:
        return {
            'status': data.get('status', 'stopped'),
            'end_time': datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            'last_updated': datetime.fromisoformat(data['last_updated']) if data.get('last_updated') else None
        }
    return {'status': 'stopped', 'end_time': None, 'last_updated': None}

# Inizializza il database se vuoto
if not timer_ref.get():
    update_timer('stopped')

# UI Streamlit
st.title("Timer Sincronizzato con Firebase")

# Recupera lo stato attuale del timer
timer_data = get_timer()

# Mostra lo stato attuale del timer
if timer_data['status'] == 'running' and timer_data['end_time']:
    remaining_time = max((timer_data['end_time'] - datetime.now()).total_seconds(), 0)
else:
    remaining_time = 0

st.write(f"Stato attuale: **{timer_data['status']}**")

if timer_data['status'] == 'running':
    st.write(f"Tempo rimanente: **{timedelta(seconds=int(remaining_time))}**")

# Input per impostare il timer
time_input = st.number_input("Imposta il timer (secondi):", min_value=1, value=60, step=1)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Avvia Timer"):
        end_time = datetime.now() + timedelta(seconds=time_input)
        update_timer('running', end_time)
        st.success("Timer avviato!")
        st.rerun()

with col2:
    if st.button("Ferma Timer"):
        update_timer('stopped')
        st.success("Timer fermato!")
        st.rerun()

with col3:
    if st.button("Aggiorna Stato"):
        st.rerun()

# Aggiornamento in tempo reale
if timer_data['status'] == 'running':
    if remaining_time > 0:
        time.sleep(1)
        st.rerun()
    else:
        update_timer('stopped')
        st.warning("Il timer è scaduto!")
        st.rerun()
