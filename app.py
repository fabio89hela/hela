# import statements
import streamlit as st
import numpy as np
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials= None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '14Bvg4LWgb0oDHr0O6fe8gbCMTvgLwlUuMaGgRx-Yxrg'
SAMPLE_RANGE_NAME = 'Sheet1!A:B'
        
service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])
stringa1="adasdskamdkam kdas sddsd sd "
stringa2=" asdasdasda sd asd asdasd"
st.title(stringa1+values[0][0]+stringa2)