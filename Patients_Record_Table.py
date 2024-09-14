import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets setup using Streamlit secrets
def setup_google_sheets():
    credentials = {
        "type": "service_account",
        "project_id": st.secrets["connections"]["gsheets"]["project_id"],
        "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
        "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["connections"]["gsheets"]["client_email"],
        "client_id": st.secrets["connections"]["gsheets"]["client_id"],
        "auth_uri": st.secrets["connections"]["gsheets"]["auth_uri"],
        "token_uri": st.secrets["connections"]["gsheets"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"]
    }
    
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Create credentials using the OAuth2 library
    creds = Credentials.from_service_account_info(credentials, scopes=scope)

    # Connect to the Google Sheets
    client = gspread.authorize(creds)
    sheet = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"]).worksheet(st.secrets["connections"]["gsheets"]["worksheet"])

    return sheet

def display_data_warehouse():
    st.title("Data Warehouse")

    # Connect to Google Sheets
    sheet = setup_google_sheets()

    # Fetch all data from the sheet
    data = sheet.get_all_records()

    # Convert data to a DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame in Streamlit
    st.dataframe(df)

# For testing the Data Warehouse functionality independently
if __name__ == "__main__":
    display_data_warehouse()
