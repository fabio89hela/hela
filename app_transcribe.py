import streamlit as st
import cdsapi
import xarray as xr
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
import os

# Funzione per scaricare i dati dal Climate Data Store (CDS)
def download_data():
    # Imposta la tua chiave API
    api_key = os.getenv('cdsapi_api_key')  

    # Crea il file .cdsapirc
    cdsapi_config = f"""
    url: https://cds.climate.copernicus.eu/api
    key: {api_key}
    verify: 1
    """
    
    # Salva il file nel percorso corretto
    with open(os.path.expanduser("~/.cdsapirc"), "w") as f:
        f.write(cdsapi_config)

    st.write("File .cdsapirc creato con successo!")

    st.write("Downloading data...")

    # Imposta i parametri per il download dei dati
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["sea_surface_temperature"],
        "year": ["2025"],
        "month": ["02"],
        "day": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12",
            "13", "14", "15",
            "16", "17", "18",
            "19", "20", "21",
            "22", "23", "24",
            "25", "26", "27",
            "28"
        ],
        "time": [
            "00:00", "01:00", "02:00",
            "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00",
            "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00",
            "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00",
            "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived"
    }

    # Crea il client CDSAPI per il download
    client = cdsapi.Client()

    # Crea un file temporaneo per salvare i dati
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nc") as tmpfile:
        file_path = tmpfile.name
        print(f"File scaricato in {file_path}")
    
    # Salva il file nel percorso del file di output
    #file_path = "downloaded_temperature_data.nc"

    # Avvia il download
    try:
        client.retrieve(dataset, request, file_path)
        if os.path.exists(file_path):
            print(f"File scaricato correttamente: {file_path}")
        else:
            raise FileNotFoundError(f"Il file non è stato scaricato in {file_path}")
    except Exception as e:
        print(f"Errore durante il download del file: {e}")
        return None
        
    st.write(f"Download completato: {file_path}")
    return file_path

# Funzione per caricare e visualizzare i dati
def load_and_display_data(file_path):
    st.write("Loading data...")

    # Carica il file NetCDF con xarray
    dataset = xr.open_dataset(file_path)
    
    # Esplora la struttura del dataset
    st.write("Dataset structure:")
    st.write(dataset)

    # Estrai i dati di temperatura (assumendo che la variabile si chiami 'sst')
    temperature_data = dataset['sst']  # Sostituisci 'sst' con il nome corretto della variabile nel tuo dataset

    # Visualizza la temperatura in un grafico
    st.write("Displaying temperature data...")
    fig, ax = plt.subplots()
    temperature_data.isel(time=0).plot(ax=ax)  # Mostra la prima istantanea temporale
    st.pyplot(fig)
    
    return dataset

# Costruisci il modello CNN
class CNNModel(nn.Module):
    def __init__(self, input_channels=1, output_size=1):
        super(CNNModel, self).__init__()
        
        # Convolutional Layer
        self.conv1 = nn.Conv2d(input_channels, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Usa un dummy input per calcolare la dimensione dell'output
        dummy_input = torch.zeros(1, input_channels, 721, 1440)
        conv_output = self.pool(torch.relu(self.conv1(dummy_input)))
        conv_out_size = conv_output.view(1, -1).size(1)

        # Fully connected layers
        self.fc1 = nn.Linear(conv_out_size, 128)
        self.fc2 = nn.Linear(128, output_size)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))  # Convolution + Pooling
        x = x.view(x.size(0), -1)  # Flatten the tensor
        x = torch.relu(self.fc1(x))  # Fully connected layer
        x = self.fc2(x)  # Output layer
        return x

# Funzione di allenamento
def train_model(model, train_loader, num_epochs=10):
    criterion = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            if inputs.dim() == 5:
                inputs = inputs.squeeze(2)
                
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        st.write(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader)}')


# Streamlit UI
def main():
    st.title("Sea Surface Temperature Prediction using CNN")
    
    st.sidebar.title("Options")
    data_option = st.sidebar.selectbox("Choose an option", ["Download and Train", "Load Existing Data"])
    
    if data_option == "Download and Train":
        file_path = download_data()
        dataset = load_and_display_data(file_path)
    else:
        uploaded_file = st.sidebar.file_uploader("Upload a NetCDF file", type=["nc"])
        if uploaded_file is not None:
            file_path = "uploaded_temperature_data.nc"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            dataset = load_and_display_data(file_path)

    st.write("Model Training")
    if st.button("Start Training"):
        model = CNNModel()
        # Preparare i dati per il training
        # Qui dovresti includere il codice per creare un DataLoader e addestrare il modello
        # Per esempio, puoi caricare un dataset fittizio per addestrare il modello
        train_loader = None  # Assicurati di impostare il train_loader correttamente
        train_model(model, train_loader, num_epochs=10)
        st.write("Training Completed!")

if __name__ == "__main__":
    main()
