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

# Input iniziale per impostare il timer
if "timer_initialized" not in st.session_state:
    st.session_state.timer_initialized = False

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

a=1   

col1, col2,col3 = st.columns([2,0.5,2]) #da usare con game
with col1:
    st.write("")
    st.write("")
    if a<4:
        st.image("logo.jpg")

with col3:
    st.write("")
    if a==0: #riscaldamento
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.link_button("Riscaldamento", "https://game.helaglobe.com/main//game?game=663-310679a7e4ef6c320734c1ff1972d769")
    elif a==1: #nuoto
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("") 
        st.link_button("Nuoto", "https://game.helaglobe.com/main//game?game=662-e68be146c4017c3e88f9a841e142e105")
    elif a==2: #ciclismo
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.link_button("Ciclismo", "https://game.helaglobe.com/main//game?game=664-b4c873aafe962e3957b1987601b9f342")
    elif a==3: #corsa
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.link_button("Corsa", "https://game.helaglobe.com/main//game?game=659-79a59a5060a0ff12333b8993dc0c1cf3")
if a==4: #timer
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
            duration_minutes = st.number_input("Durata del timer (in minuti):", min_value=0.00, max_value=60.00, value=None)
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
                    if seconds<=10 and minutes==0:
                        st.markdown(
                        f"""
                        <p style="font-size: 70px; font-weight: bold; text-align: center;color: #ff4b4b;">
                        Tempo rimanente: {seconds:02d}
                        </p>
                        """,
                        unsafe_allow_html=True
                            )
                    else:
                        st.markdown(
                        f"""
                        <p style="font-size: 50px; font-weight: bold; text-align: center;">
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
                        stop_timer()
                        st.session_state.timer_initialized = False
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
            time.sleep(0.05)
            st.rerun()
