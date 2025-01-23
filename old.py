import firebase_admin
from firebase_admin import credentials, db

# Credenziali Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "aiom---torino",
    "private_key_id": "00a8acd641b985579bccb3b0deaed42342cb278b",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCXAd6I9OQR7Bs4\n...",
    "client_email": "firebase-adminsdk-fbsvc@aiom---torino.iam.gserviceaccount.com",
    "client_id": "111890186751886728605",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40aiom---torino.iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://aiom---torino-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Riferimento al database
ref = db.reference('test')

# Prova di scrittura
ref.set({'status': 'connection_successful'})

# Prova di lettura
data = ref.get()
print("Dati letti dal database:", data)
