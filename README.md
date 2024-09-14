# Patient Record Management System

## Overview

The Patient Record Management System is a web application built using Streamlit, designed to manage patient records efficiently. The application allows users to log in, manage patient data, visualize data, and configure settings. It uses environment variables for sensitive data management and integrates with Google Sheets for data storage.

## Features

- **User Authentication**: Secure login functionality with username and password authentication.
- **Data Collection**: Input and manage patient records.
- **Data Warehouse**: View and manage data stored in Google Sheets.
- **Data Visualization**: Generate and view visualizations of patient data.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- dotenv
- Google Sheets API client (if integrating with Google Sheets)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/patient-record-management.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd patient-record-management
    ```

3. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file in the root directory of the project with your environment variables:**

    ```plaintext
    APP_USERNAME=your-username
    APP_PASSWORD=your-password
    ```

### Running the Application

1. **Start the Streamlit server:**

    ```bash
    streamlit run app.py
    ```

2. **Open your web browser and navigate to `http://localhost:8501` to use the application.**

### Application Structure

- **`app.py`**: Main entry point for the Streamlit app. Handles navigation and displays the different pages.
- **`login.py`**: Contains the login functionality.
- **`data_warehouse.py`**: Displays data from Google Sheets.
- **`data_collection.py`**: Manages data collection and input.
- **`data_visualization.py`**: Provides data visualization functionalities.

### Contact

For any questions or issues, please contact gm.baltistani1@gmail.com
