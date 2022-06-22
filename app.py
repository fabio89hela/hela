import streamlit as st
import pandas as pd
import datetime
#import pywhatkit
import time
import pyautogui
import keyboard as k

#pywhatkit.sendwhats_image("+39xxx", "C:\\Users\\tedon\\Desktop\\download.jpg", "Esempio", 10, False, 5)
st.write("Scegli il file excel")
uploaded_file = st.file_uploader("Scegli un file")
if uploaded_file is not None:
	df = pd.read_excel(uploaded_file)
	st.write(df)
	testo1 = st.text_input('Testo da inviare prima del nome', '')
	testo2 = st.text_input('Testo da inviare dopo il nome', '')
	submit = st.button("Invia")
	if submit:
		for i in df.index:
			#numero="+39"+str(df["Numero"][i])
			#pywhatkit.sendwhatmsg_instantly(numero, testo1+df["Nome"][i]+testo2,15,False,3)
			w=pyautogui.size().width
			h=pyautogui.size().height
			pyautogui.click(w*0.65,h*0.8)
			k.press_and_release('enter')
		st.success("Messaggi inviati!")
