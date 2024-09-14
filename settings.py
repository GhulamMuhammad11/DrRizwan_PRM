import streamlit as st

def settings_page():
    st.title("Settings Page")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.query_params(page="login")
        st.session_state.page = "login"

def logout():
    if st.session_state.authenticated:
        settings_page()
    else:
        st.query_params(page="login")
        st.session_state.page = "login"
