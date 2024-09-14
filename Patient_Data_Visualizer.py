import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re  # To extract years from the 'Age' column
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

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_info(credentials, scopes=scope)

    client = gspread.authorize(creds)
    sheet = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"]).worksheet(st.secrets["connections"]["gsheets"]["worksheet"])

    return sheet

def load_data(sheet):
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    
    # Convert all values in 'Age' column to string
    df['Age'] = df['Age'].apply(lambda x: str(x) if not pd.isna(x) else '')
    
    # Extract numerical 'Age' from strings like "0 years 0 months and 0 days old"
    df['Age'] = df['Age'].apply(extract_years)
    
    return df

# Helper function to extract years from the age string
def extract_years(age_string):
    match = re.search(r'(\d+)\s+years', age_string)
    if match:
        return int(match.group(1))
    else:
        return 0  # Default to 0 if no years are found

def plot_graphs(df):
    st.title("Data Visualization")
    
    # Age distribution
    st.subheader("Age Distribution")
    plt.figure(figsize=(15, 5))
    sns.histplot(df['Age'], bins=20, kde=True)
    st.pyplot(plt.gcf())

    # Sex distribution
    st.subheader("Sex Distribution")
    plt.figure(figsize=(15, 5))
    sns.countplot(x='Sex', data=df)
    st.pyplot(plt.gcf())

    # Marital Status distribution
    st.subheader("Marital Status Distribution")
    plt.figure(figsize=(15, 5))
    sns.countplot(x='Marital Status', data=df)
    st.pyplot(plt.gcf())

    # Provisional Diagnosis word cloud (if applicable)
    st.subheader("Provisional Diagnosis Word Cloud")
    try:
        from wordcloud import WordCloud
        text = ' '.join(df['Provisional Dx'].dropna())
        wordcloud = WordCloud(width=600, height=300, background_color='white').generate(text)
        plt.figure(figsize=(15, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt.gcf())
    except ImportError:
        st.warning("WordCloud library not installed. Please install it to visualize word clouds.")

    # Further graphs (up to 15) can be added below
    checkbox_columns = ['Jaundice', 'Pallor', 'Koilonychia', 'Lymph Nodes']
    for col in checkbox_columns:
        st.subheader(f"{col} Distribution")
        plt.figure(figsize=(15, 5))
        sns.countplot(x=col, data=df)
        st.pyplot(plt.gcf())

def data_visualization():
    sheet = setup_google_sheets()
    df = load_data(sheet)
    plot_graphs(df)
