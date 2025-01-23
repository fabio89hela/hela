import streamlit as st
import time

# Configurazione della pagina
st.set_page_config(page_title="Timer Condiviso", layout="centered")

# Titolo
st.title("Timer Condiviso")

# Inizializzazione dello stato del timer
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.remaining_time = 0

# Funzione per avviare il timer
def start_timer(duration):
    st.session_state.timer_running = True
    st.session_state.start_time = time.time()
    st.session_state.remaining_time = duration

# Funzione per fermare il timer
def stop_timer():
    st.session_state.timer_running = False
    st.session_state.start_time = None
    st.session_state.remaining_time = 0

# Input per la durata del timer (solo per chi lo avvia)
if not st.session_state.timer_running:
    duration_minutes = st.number_input("Durata del timer (in minuti):", min_value=1, max_value=60, value=5)
    if st.button("Avvia Timer"):
        start_timer(duration_minutes * 60)

# Timer attivo
if st.session_state.timer_running:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, st.session_state.remaining_time - elapsed_time)

    # Visualizzazione del timer
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    st.subheader(f"Tempo rimanente: {minutes:02d}:{seconds:02d}")

    # Controllo se il timer è scaduto
    if remaining_time <= 0:
        st.success("Il timer è scaduto!")
        stop_timer()

    # Pulsante per fermare manualmente il timer
    if st.button("Ferma Timer"):
        stop_timer()

# Istruzioni per chi accede successivamente
if not st.session_state.timer_running:
    st.info("Il timer non è attivo. Puoi avviarne uno nuovo.")

# Aggiorna la pagina ogni secondo per sincronizzare il timer
if st.session_state.timer_running:
    time.sleep(1)
    st.experimental_rerun()
