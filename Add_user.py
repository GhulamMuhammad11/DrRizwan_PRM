#===================================================Import Necessary Libraries================================================================

from altair import Align
import streamlit as st
from datetime import datetime
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
import pandas as pd
import pdfkit
import base64

#===================================================Google drive and sheets authentication=====================================================

# Google Sheets setup using Streamlit secrets
def setup_google_sheets():
    # Load credentials from the secrets.toml file
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

#===================================================Save to google sheets================================================================

def save_to_google_sheets(sheet, data):
    # Convert date fields to strings if necessary
    for i, item in enumerate(data):
        for key, value in item.items():
            if isinstance(value, (datetime, pd.Timestamp)):
                item[key] = value.strftime('%Y-%m-%d')
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    # Append data to Google Sheets
    for _, row in df.iterrows():
        sheet.append_row(row.tolist())

#===================================================Add User================================================================

def data_collection():

    #==============================Personal Information=============================================
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h1 style='font-size: 38px; margin: 0; padding: 0;'>Manzoor Medical Hall And Children Clinic</h1>
        <h2 style='font-size: 15px; margin: 0;'>120, THE LOWER MALL, MURREE. PH: 051-3410649. EMAIL: auzain@gmail.com</h2>
    </div>
    """, 
    unsafe_allow_html=True
)
   

    logo_path = "logo1.bmp"

    col1, col2, col3 = st.columns(3)

    with col1:
            st.markdown(
    """ <h2 style='font-size: 32px; margin: 0; padding: 0;'>Dr.Mirza Rizwan UI Hassan</h2>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>MBBS(Pb) R.M.PPMDC NO:24957-P</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>PHC.REG.NO.R-02568</h3>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>FAMILY & PEDIATRIC PHYSICIAN</h3>
    """, 
    unsafe_allow_html=True
)        
    with col2:
        st.image(logo_path, width=200)
    with col3:
        st.markdown(
    """ <h3 style='font-size: 15px; margin: 0; padding: 0;'>DIPLOMA IN FAMILY MEDICINE (HSA) Pakistan </h3>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>DIPLOMA IN PEDIATRICS (RCPI) Ireland </h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>DCH (IHMS) Pakistan </h3>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>CERTIFIED IN FAMILY MEDICINE (CIFM) Lahore</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>CERTIFIED IN BASIC LIFE SUPPORT (SHIFA) 18L</h3>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>PGPN BOSTON UNIVERSITY (USA)  </h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>ENS (LMO University) Germany </h3>
        <h3 style='font-size: 15px; margin: 0;padding: 0;'>SKGCHC (SickKids Hospital) Canada</h3>
    """, 
    unsafe_allow_html=True
)        
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h2 style='font-size: 20px;'>========================================</h2>
    </div>
    """, 
    unsafe_allow_html=True)
    
    st.header("Personal Information")

    today = datetime.today()
    min_years_ago = today.replace(year=today.year - 150)
    max_years_from_now = today.replace(year=today.year + 50)
    with st.container():
        col1, col2, col3 = st.columns(3)
        dated = col1.date_input("Dated", min_value=min_years_ago, max_value=max_years_from_now)
        mr_no = col2.text_input("MR No")
        name = col3.text_input("Name")
        father_name = col1.text_input("Father Name")
        dob = col2.date_input("Date of Birth", min_value=min_years_ago, max_value=max_years_from_now)
        weight = col3.text_input("Weight")
        occupation = col1.text_input("Occupation")
        contact_no = col2.text_input("Contact No")
        cnic_no = col3.text_input("CNIC No")

        # Age input with days, months, and years
        # col1.write("Age")
        age_days = col1.number_input("Age(Days)", min_value=0, max_value=31, format="%d")
        age_months = col2.number_input("Age(Months)", min_value=0, max_value=12, format="%d")
        age_years = col3.number_input("Age(Years)", min_value=0, format="%d")

        marital_status = col3.radio("Marital Status", ('Single', 'Married', 'Divorced','Widow','Other'))
        sex = col1.radio("Sex", ('Male', 'Female', 'Other'))
        category = col2.radio("Category", ['Deserving', 'Non-Deserving','other'])
        father_occup = st.text_input("Father Occupation")

        address = st.text_area("Address")

    #============================================Emergency Assessment====================================================
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h2 style='font-size: 20px;'>========================================</h2>
    </div>
    """, 
    unsafe_allow_html=True)

    st.header("Emergency assessment")

    # Checklist for Emergency Assessment
    with st.container():
        st.write("A: Airway")

        col1, col2, col3, col4 = st.columns(4)

        secretions = col1.checkbox("Secretions")
        secretions_details = col1.text_input("Details for Secretions")

        stridor = col2.checkbox("Stridor")
        stridor_details = col2.text_input("Details for Stridor")

        foreign_body = col3.checkbox("Foreign Body")
        foreign_body_details = col3.text_input("Details for Foreign Body")

        st.write("B: Breathing")
        col1, col2, col3, col4 = st.columns(4)

        respiratory_rate = col1.checkbox("Respiratory Rate")
        respiratory_rate_details = col1.text_input("Details for Respiratory Rate")

        retractions = col2.checkbox("Retractions/Accessory Muscle Use")
        retractions_details = col2.text_input("Details for Retractions")

        oxygen_saturation = col3.checkbox("Oxygen Saturation")
        oxygen_saturation_details = col3.text_input("Details for Oxygen Saturation")

        auscultation = col4.checkbox("Auscultation")
        auscultation_details = col4.text_input("Details for Auscultation")

        st.write("C: Circulation")
        col1, col2, col3, col4 = st.columns(4)

        color = col1.checkbox("Color (e.g., pale or mottled)")
        color_details = col1.text_input("Details for Color")

        heart_rate = col2.checkbox("Heart Rate")
        heart_rate_details = col2.text_input("Details for Heart Rate")

        capillary_refill = col3.checkbox("Capillary Refill")
        capillary_refill_details = col3.text_input("Details for Capillary Refill")

        temp_hands_feet = col4.checkbox("Temperature of the Hands and Feet")
        temp_hands_feet_details = col4.text_input("Details for Hands/Feet Temperature")

        st.write("D: Disability")
        col1, col2, col3, col4 = st.columns(4)

        pupils = col1.checkbox("Pupils")
        pupils_details = col1.text_input("Details for  Pupils")

        limb_tone = col2.checkbox("Limb Tone & Movement")
        limb_tone_details = col2.text_input("Details for  limb_tone")

        avpu = col3.checkbox("AVPU Score/GCS")
        avpu_details = col3.text_input("Details for  avpu")

        glucose = col4.checkbox("Glucose")
        glucose_details = col4.text_input("Details for glucose")

        # st.write("ENT: Ear, Nose & Throat Examination")
        ent_examination = st.text_area("Ear, Nose & Throat Examination")

        # st.write("T: Temperature")
        temperature = st.text_area("Temperature")

        # st.write("T: Tummy")
        tummy = st.text_area("Tummy Examination")

        # st.write("If Drowsy or Very Unwell, Include:")
        defg_glucose = st.text_area("DEFG– And Don’t Ever Forget Glucose")

    #==================================================Medical Information========================================
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h2 style='font-size: 20px;'>========================================</h2>
    </div>
    """, 
    unsafe_allow_html=True)

    st.header("Medical Information")

    with st.container():
        chief_complaints = st.text_area("Chief Complaints")
        hopi = st.text_area("HOPI")
        past_hx = st.text_area("Past History")
        birth_hx = st.text_area("Birth History")
        immunization = st.text_area("Immunization")
        developmental_hx = st.text_area("Developmental History")
        family_hx = st.text_area("Family History")
        allergies = st.text_area("Allergies")
        drug_hx = st.text_area("Drug History")
        social_hx = st.text_area("Social History")
        antenatal_gynal_obs = st.text_area("ANTENATAL/GYNAL/OBS")

    #==============================================Physical Examination==================================================
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h2 style='font-size: 20px;'>========================================</h2>
    </div>
    """, 
    unsafe_allow_html=True)

    st.header("Physical Examination")
    
    st.write("General Physical Examination(GPE)")
    col1, col2, col3, col4 = st.columns(4)


    jaundice = col1.checkbox("Jaundice")
    Jaundice_details = col1.text_input("Details for Jaundice")

    pallor = col2.checkbox("Pallor")
    Pallor_details = col2.text_input("Details for Pallor")

    koilonychia = col3.checkbox("Koilonychia")
    Koilonychia_details = col3.text_input("Details for Koilonychia")

    lymph_nodes = col4.checkbox("Lymph Nodes")
    Lymph_details = col4.text_input("Details for Lymph")

    
    st.write("Vital Signs")
    col1, col2, col3, col4 = st.columns(4)

    rr = col1.checkbox("Respiratory_Rate")
    rr_details = col1.text_input("Details for Respiratory_Rate")

    hr = col2.checkbox("Heart_Rate")
    hr_details = col2.text_input("Details for Heart_Rate")

    bp = col3.checkbox("Blood Pressure")
    bp_details = col3.text_input("Details for Blood Pressure")

    temp = col4.checkbox("Temperature")
    temp_details = col4.text_input("Details for Temperature")


    st.write("Respiratory System")
    col1, col2, col3, col4, col5 = st.columns(5)

    git = col1.checkbox("GIT (Gastrointestinal Tract)")
    git_details = col1.text_input("Details for GIT")

    cns = col2.checkbox("CNS (Central Nervous System)")
    cns_details = col2.text_input("Details for CNS")

    cvs = col3.checkbox("CVS (Cardiovascular System)")
    cvs_details = col3.text_input("Details for CVS")

    ent = col4.checkbox("ENT (Ear Nose Throat)")
    ent_details = col4.text_input("Details for ENT")

    thyroid = col5.checkbox("Thyroid")
    thyroid_details = col5.text_input("Details for Thyroid")

    #=========================================Provisional Diagnosis============================================
    st.markdown(
    """
    <div style='text-align: center; line-height: -2;'>
        <h2 style='font-size: 20px;'>========================================</h2>
    </div>
    """, 
    unsafe_allow_html=True)

    st.header("Provisional Diagnosis")

    provisional_dx = st.text_area("Provisional Diagnosis")
    investigations = st.text_area("Investigations")
    treatment = st.text_area("Treatment")
    follow_up = st.text_area("Follow up")
    final_diagnosis = st.text_area("Final Diagnosis")
    final_investigations = st.text_area("Final Investigations")

    #=======================================Submit Button======================================================
    # Add a submit button
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
    if st.button("Submit"):
        # Prepare data to be saved
        data = {
            'Dated': dated,
            'MR No': mr_no,
            'Name': name,
            'Father Name': father_name,
            'Date of Birth': dob,
            'weight': weight,
            'Occupation': occupation,
            'Contact No': contact_no,
            'Age': f"{age_years} years {age_months} months and {age_days} days old",
            'Marital Status': marital_status,
            'CNIC No': cnic_no,
            'Sex': sex,
            'Category': category,
            'father_occupation': father_occup,
            'Address': address,
            'Secretions': secretions,
            'Secretions_details': secretions_details,
            'Stridor': stridor,
            'Stridor_details': stridor_details,
            'Foreign Body': foreign_body,
            'Foreign_Body_details': foreign_body_details,
            'Respiratory Rate': respiratory_rate,
            'Respiratory Rate_details': respiratory_rate_details,
            'Retractions/Accessory Muscle Use': retractions,
            'Retractions/Accessory Muscle Use details': retractions_details,
            'Oxygen Saturation': oxygen_saturation,
            'Oxygen Saturation details': oxygen_saturation_details,
            'Auscultation': auscultation,
            'Auscultation_details': auscultation_details,
            'Color': color,
            'Color_details': color_details,
            'Heart Rate': heart_rate,
            'Heart Rate_details': heart_rate_details,
            'Capillary Refill': capillary_refill,
            'Capillary Refill detail': capillary_refill_details,
            'Temperature of the Hands and Feet': temp_hands_feet,
            'Temperature of the Hands and Feet details': temp_hands_feet_details,
            'Pupils': pupils,
            'Pupils_details': pupils_details,
            'Limb Tone & Movement': limb_tone,
            'Limb Tone & Movement_details': limb_tone_details,
            'AVPU Score/CGS': avpu,
            'AVPU Score/CGS_details': avpu_details,
            'Glucose': glucose,
            'Glucose_details': glucose_details,
            'ENT Examination': ent_examination,
            'Temperature': temperature,
            'Tummy Examination': tummy,
            'DEFG Glucose': defg_glucose,
            'Chief Complaints': chief_complaints,
            'HOPI': hopi,
            'Past HX': past_hx,
            'Birth HX': birth_hx,
            'Immunization': immunization,
            'Developmental HX': developmental_hx,
            'Family HX': family_hx,
            'Allergies': allergies,
            'Drug HX': drug_hx,
            'Social HX': social_hx,
            'ANTENATAL/GYNAL/OBS': antenatal_gynal_obs,
            'Jaundice': jaundice,
            'Jaundice_details': Jaundice_details,
            'Pallor': pallor,
            'Pallor_details': Pallor_details,
            'Koilonychia': koilonychia,
            'Koilonychia_details': Koilonychia_details,
            'Lymph Nodes': lymph_nodes,
            'Lymph Nodes_details': Lymph_details,
            'RR': rr,
            'RR_details': rr_details,
            'HR': hr,
            'HR_details': hr_details,
            'BP': bp,
            'BP_details': bp_details,
            'Temp': temp,
            'Temp_details': temp_details,
            'GIT': git,
            'GIT_details': git_details,
            'CNS': cns,
            'CNS_details': cns_details,
            'CVS': cvs,
            'CVS_details': cvs_details,
            'ENT': ent,
            'ENT_details': ent_details,
            'Thyroid': thyroid,
            'Thyroid_details': thyroid_details,
            'Provisional Dx': provisional_dx,
            'Investigations': investigations,
            'Treatment': treatment,
            'Follow up': follow_up,
            'Final Diagnosis': final_diagnosis,
            'Final Investigations': final_investigations
        }       
        
        # Convert date fields to strings
        data['Dated'] = data['Dated'].strftime('%Y-%m-%d')
        data['Date of Birth'] = data['Date of Birth'].strftime('%Y-%m-%d')

        # Connect to Google Sheets
        sheet = setup_google_sheets()
        save_to_google_sheets(sheet, [data])
        st.success("Data has been saved to Google Sheets!")

    #===================================================Generate PDF=========================================================================
    # Path to wkhtmltopdf binary
    path_wkhtmltopdf = 'https://github.com/GhulamMuhammad11/DrRizwan_PRM/blob/834b740bd08f1fbc7b35e24a15d37dfdc03b0992/wkhtmltox-0.12.6-1.amazonlinux2.aarch64.rpm'  # Update with the actual path in your repo
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    # Function to generate PDF from HTML content
    def generate_pdf(html_content, output_filename):
        # pdfkit.from_string(html_content, output_filename)
        pdfkit.from_string(html_content, output_filename, configuration=config)

    # Function to encode image to base64
    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    # Generate the HTML content
    def create_patient_report():
        logo_base64 = encode_image_to_base64('logo1.bmp')  # Provide the path to your logo image
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .container {{
                    text-align: center;
                    line-height: -2;
                    font-family: Arial, sans-serif;
                }}
                .header {{
                    margin: 0;
                    padding: 0;
                }}
                .logo {{
                    width: 200px;
                    margin: 0 auto;
                }}
                .column {{
                    display: inline-block;
                    vertical-align: top;
                    width: 30%;
                    padding: 10px;
                }}
                .column h2, .column h3 {{
                    margin: 0;
                    padding: 0;
                    font-size: 15px;
                }}
                .title {{
                    font-size: 38px;
                    margin: 0;
                    padding: 0;
                }}
                .subtitle {{
                    font-size: 15px;
                    margin: 0;
                }}
                .left-align {{
                    text-align: left;
                    margin-left: 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="title">Manzoor Medical Hall And Children Clinic</h1>
                    <h2 class="subtitle">120, THE LOWER MALL, MURREE. PH: 051-3410649. EMAIL: auzain@gmail.com</h2>
                </div>
                <div class="column left-align" style="width: 30%;">
                    <h2 style='font-size: 20px;'>Dr. Mirza Rizwan UI Hassan</h2>
                    <h3 style='font-size: 15px;'>MBBS(Pb) R.M.PPMDC NO:24957-P</h3>
                    <h3 style='font-size: 15px;'>PHC.REG.NO.R-02568</h3>
                    <h3 style='font-size: 15px;'>FAMILY & PEDIATRIC PHYSICIAN</h3>
                </div>
                <div class="column">
                    <img src="data:image/bmp;base64,{logo_base64}" alt="Clinic Logo" class="logo">
                </div>
                <div class="column left-align" style="width: 30%;">
                    <h3 style='font-size: 15px;'>DIPLOMA IN FAMILY MEDICINE (HSA) Pakistan</h3>
                    <h3 style='font-size: 15px;'>DIPLOMA IN PEDIATRICS (RCPI) Ireland</h3>
                    <h3 style='font-size: 15px;'>DCH (IHMS) Pakistan</h3>
                    <h3 style='font-size: 15px;'>CERTIFIED IN FAMILY MEDICINE (CIFM) Lahore</h3>
                    <h3 style='font-size: 15px;'>CERTIFIED IN BASIC LIFE SUPPORT (SHIFA) 18L</h3>
                    <h3 style='font-size: 15px;'>PGPN BOSTON UNIVERSITY (USA)</h3>
                    <h3 style='font-size: 15px;'>ENS (LMO University) Germany</h3>
                    <h3 style='font-size: 15px;'>SKGCHC (SickKids Hospital) Canada</h3>
                </div>
                <div class="column centre" style="width: 30%;">
                    <h2 style='font-size: 20px;'>-------------------------------------</h2>
                </div>
            </div>
        </body>
        </html>
        """
        # Generate PDF from the HTML content
        output_filename = f'{mr_no}_patient_report.pdf'
        generate_pdf(html_content, output_filename)

        return output_filename

    if st.button("Generate Patient Report PDF"):
            pdf_file = create_patient_report()
            
            # Provide download link for the generated PDF
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name="patient_report.pdf",
                    mime="application/octet-stream"
                )
                
    st.markdown(
            """
        <div style='text-align: left; line-height: -10;'>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>Developed by:</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>Ghulam Muhammad, Artificial Intelligence Researcher</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>MSISLAB</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>MSISLab.com</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>Email: gm.baltistani1@gmail.com </h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>Phone: +92-334-8841108</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>304, E9, ChungBuk National Univ.</h3>
        <h3 style='font-size: 15px; margin: 0; padding: 0;'>ChengJu-si, ChungCheongBuk-do, South Korea</h3>
    """, 
    unsafe_allow_html=True
        )


    




        