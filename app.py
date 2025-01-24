import streamlit as st
import time

a=0

st.title("AIOM - TORINO")
if a==0:
    st.link_button("Riscaldamento", "https://game.helaglobe.com/main//game?game=623-8bb7fe84d0c4823efd469dfbf2dccc13")
elif a==1:
    st.link_button("Corsa", "https://game.helaglobe.com/main//game?game=624-3feefa2ef9a347a0423cc694246871c7")
time.sleep(1)
st.rerun()
    
