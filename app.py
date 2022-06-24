import os
os.environ['DISPLAY']=':0'
os.environ['XAUTHORITY']='/run/user/1000/gdm/Xauthority'
import streamlit as st
import pandas as pd
import pywhatkit
import pyautogui
from PIL import Image

stringa_xls="C:\\Users\\tedon\\Desktop\\numeri.xlsx"
st.title("Benvenuto!")
st.write("Da questa pagina potrai gestire le tue comunicazioni whatsapp")
check=st.checkbox("Voglio scegliere il file dei contatti")
if check==True:
	uploaded_file=st.file_uploader("Scegli il file excel",['xls','xlsx'])
else:
	uploaded_file=stringa_xls
if uploaded_file is not None:
	df = pd.read_excel(uploaded_file)
	uploaded_image=st.file_uploader("Scegli l'immagine da inviare",['png','jpg','jpeg'])
	if uploaded_image is not None: 
		image=Image.open(uploaded_image)
		st.image(image,width=200)	
		testo1 = st.text_input('Testo da inviare prima del nome ', '')
		testo2 = st.text_input('Testo da inviare dopo il nome ', '')
		submit = st.button("Invia")
		if submit:
			for k in range(len(df)):
				pywhatkit.sendwhats_image("+39"+str(df["Numero"][k]), uploaded_image, testo1+" "+str(df["Nome"][k])+" "+testo2, 25, True, 10) 
			st.write("Fatto")
