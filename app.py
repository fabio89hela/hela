# import statements
import streamlit as st
import numpy as np
import mediapipe as mp
import cv2
import tempfile
import time
from PIL import Image
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="example")
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

st.title('Controllo del volto')
st.markdown (
	"""
	<style>
	[data-testid="stSidebar"][aria-expanded="true"]>div:first-child{
		width:350px
	}
	[data-testid="stSidebar"][aria-expanded="false"]>div:first-child{
		width:350px
		margin-left:-350px
	}
	</style>
	""",
	unsafe_allow_html=True,
)

st.sidebar.title('Menù')
st.sidebar.subheader('parametri')

@st.cache()
def image_resize(image,width=None,height=None,inter =cv2.INTER_AREA):
	dim=None
	(h,w)=image.shape[:2]
	
	if width is None and height is None:
		return image
	
	if width is None:
		r=width/float(w)
		dim=(int(w*r).height)
	
	else:
		r=width/float(w)
		dim=(width,int(h*r))
	
	#ridimensiona l'immagine
	resized=cv2.resize(image,dim,interpolation=inter)
	
	return resized
	
app_mode=st.sidebar.selectbox('Scegli la modalità',['Immagine','Video'])

if app_mode=='Immagine':
	st.sidebar.markdown('---')
	st.markdown (
	"""
	<style>
	[data-testid="stSidebar"][aria-expanded="true"]>div:first-child{
		width:350px
	}
	[data-testid="stSidebar"][aria-expanded="false"]>div:first-child{
		width:350px
		margin-left:-350px
	}
	</style>
	""",
	unsafe_allow_html=True,
	)

	st.sidebar.markdown('---')
	detection_confidence=st.sidebar.slider('Confidenza modello',min_value=0.0,max_value=1.0,value=0.5)
	st.sidebar.markdown('---')
	img_file_buffer=st.sidebar.file_uploader("Scegli un'immagine",type=["jpg","jpeg","png"])
	if img_file_buffer is not None:
		image=np.array(Image.open(img_file_buffer))
		st.sidebar.text("Immagine originale")
		st.sidebar.image(image)
		face_count=0
		#Dashboard
		with mp_pose.Pose(
			static_image_mode=True,
			model_complexity=2,
			enable_segmentation=True,
			min_detection_confidence=detection_confidence) as pose:
			image_height, image_width, _ = image.shape
			# Convert the BGR image to RGB before processing.
			results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
			out_image = image.copy()
			# Draw pose landmarks on the image.
			mp_drawing.draw_landmarks(
			out_image,
			results.pose_landmarks,
			mp_pose.POSE_CONNECTIONS,
			landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
			mp_drawing.plot_landmarks(
				results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
			st.subheader('Output')
			st.image(out_image,use_column_width=True)

	
	