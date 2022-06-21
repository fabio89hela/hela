import streamlit as st
import pandas as pd

st.write("Scegli il file excel")
uploaded_file = st.file_uploader("Scegli un file")
if uploaded_file is not None:
	df = pd.read_excel(uploaded_file)
	st.write(df)
