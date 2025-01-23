import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import logging



# Verifica se l'app Firebase è già stata inizializzata
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

    firebase_admin._http_client.logging.getLogger().setLevel(logging.DEBUG)
    # Testa scrittura e lettura
    ref = db.reference("test")
    try:
        ref.set({"status": "connection_successful"})  # Scrive nel database
        print(ref.get())  # Legge dal database
    except Exception as e:
        print("Errore:", e)

# Riferimento al database
ref = db.reference('test')

# Prova di scrittura
ref.set({'status': 'connection_successful'})

# Prova di lettura
data = ref.get()
print("Dati letti dal database:", data)
