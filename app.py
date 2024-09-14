from login import login_page
import streamlit as st
from Patients_Record_Table import display_data_warehouse
from Add_user import data_collection
from Patient_Data_Visualizer import data_visualization
from settings import logout


def main():
    if login_page():

        st.set_page_config(layout="wide")
        
        with st.sidebar:
            st.header("Dashboard")
            page = st.radio("Go to", ["Add Records", "Patients Records Table", "Patients Data Visualizer"])

        if page == "Add Records":
            data_collection() 
        elif page == "Patients Records Table":
            display_data_warehouse()
        elif page == "Patients Data Visualizer":
            data_visualization()
        elif page == "Settings":
            pass
    
if __name__ == "__main__":
    main()
