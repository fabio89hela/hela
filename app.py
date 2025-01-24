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

a=4

col1, col2 = st.columns(2)
with col1:
    st.image("logo.jpg")

with col2:
    st.write("")
    if a==0: #riscaldamento
        st.link_button("Riscaldamento", "https://game.helaglobe.com/main//game?game=623-8bb7fe84d0c4823efd469dfbf2dccc13")
    elif a==1: #nuoto
        st.link_button("Nuoto", "https://game.helaglobe.com/main//game?game=626-ddaf247e22a4a397e13e43e8b7f65572")
    elif a==2: #ciclismo
        st.link_button("Ciclismo", "https://game.helaglobe.com/main//game?game=625-241ca8173c27da5c6db93d8028cfe264")
    elif a==3: #corsa
        st.link_button("Corsa", "https://game.helaglobe.com/main//game?game=624-3feefa2ef9a347a0423cc694246871c7")
    elif a==4: #timer
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
                    minutes = int(remaining_time // 60)
                    seconds = int(remaining_time % 60)
                    if seconds<=10:
                        st.markdown(
                    f"""
                    <p style="font-size: 48px; font-weight: bold; text-align: center;color: #ff4b4b;">
                    Tempo rimanente: {minutes:02d}:{seconds:02d}
                    </p>
                    """,
                    unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                    f"""
                    <p style="font-size: 48px; font-weight: bold; text-align: center;">
                    Tempo rimanente: {minutes:02d}:{seconds:02d}
                    </p>
                    """,
                    unsafe_allow_html=True
                        )
    
                    # Fermare il timer
                    if st.button("Ferma Timer", key="stop_button"):
                        stop_timer()
                        st.session_state.timer_initialized = False

                    # Mostra messaggio quando scade
                    if remaining_time <= 0:
                        st.success("Il timer è scaduto!")
                        stop_timer()
                        st.session_state.timer_initialized = False
                        st.markdown(
                        """
                        <audio autoplay>     
                            <source src="https://drive.google.com/file/d/10zYKOPqoaSUVTEic76mov04KwYXuhqjE/view?usp=sharing" type="audio/mp3">
                            Il tuo browser non supporta l'elemento audio.
                        </audio>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.session_state.timer_initialized = False

            # Ottieni nuovamente lo stato del timer dal database
            timer_data = timer_ref.get()
            if not timer_data:
                timer_data = {"start_time": None, "duration": 0, "running": False}

            running = timer_data.get("running", False)
            start_time = timer_data.get("start_time", None)
            duration = timer_data.get("duration", 0)

            # Aspetta 1 secondo prima di aggiornare
            time.sleep(0.8)
            st.rerun()
