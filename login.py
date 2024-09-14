#login page code
import os
import streamlit as st
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Function to check if the username and password are correct
def is_authenticated(username, password):
    # stored_username = st.secrets["authentication"]["APP_USERNAME"]
    # stored_password = st.secrets["authentication"]["APP_PASSWORD"]
    stored_username = os.getenv("APP_USERNAME")
    stored_password = os.getenv("APP_PASSWORD")
    
    if not stored_username or not stored_password:
        st.error("Environment variables for username and password are not set.")
        return False
    
    return username == stored_username and password == stored_password


# Function to handle login
def handle_login(username, password):
    if is_authenticated(username, password):
        st.session_state.authenticated = True
        st.session_state.login_success = True
        with st.spinner("Loading..."):
            time.sleep(2)
    else:
        st.session_state.login_success = False
        st.error("Invalid username or password")

# Main function for the login page
def login_page():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "login_success" not in st.session_state:
        st.session_state.login_success = None

    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        .login-title {
            font-size: 48px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
        }
        .stTextInput label {
            font-size: 20px;
            font-weight: 500;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="login-title">Login Page</p>', unsafe_allow_html=True)

               
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        
        st.markdown("""
            <style>
            .stButton button {
                border-radius: 12px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
            }
            .stButton button:hover {
                background-color: #45a049;
            }
            .stButton button {
                width: 100%;
            }
            </style>
            """, unsafe_allow_html=True)
        
        login_button = st.button("Login", on_click=lambda: handle_login(login_username, login_password))

    return st.session_state.authenticated