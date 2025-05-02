import streamlit as st
import pandas as pd
import hashlib
import os
import time
import base64
import pickle
import numpy as np
from fpdf import FPDF
from sklearn.preprocessing import StandardScaler 
from datetime import datetime
import base64
from joblib import load
from PIL import Image

scaler = StandardScaler()

# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

#Done Diabetes
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))#231
#Done Heart
heart_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
#Done Hypertension
hyp_model = pickle.load(open(f'{working_dir}/saved_models/hyp_model.sav', 'rb'))
#Done Stroke
stroke_model = pickle.load(open(f'{working_dir}/saved_models/stroke_model.sav', 'rb'))
 
migraine_model = pickle.load(open(f'{working_dir}/saved_models/maigraine_model.sav', 'rb'))
#Done Lung_cancer
lc_model = pickle.load(open(f'{working_dir}/saved_models/lc_model.sav', 'rb'))
#Done Kidney_stone
ks_model = pickle.load(open(f'{working_dir}/saved_models/ks_model.sav', 'rb'))
#Done Heart_Failure
heartF_model = pickle.load(open(f'{working_dir}/saved_models/heart_failure_model.sav', 'rb'))
#Done COPD
copd_model = pickle.load(open(f'{working_dir}/saved_models/copd_model.sav', 'rb'))
#Done Thyroid
thyroid_model=pickle.load(open(f'{working_dir}/saved_models/thyroid_model.sav', 'rb'))
#
sleepD_model=pickle.load(open(f'{working_dir}/saved_models/sleepdis_model.sav', 'rb'))
#obesity
Obesity_model=pickle.load(open(f'{working_dir}/saved_models/obesity_model.sav', 'rb'))
#Done AIDS
aids_model = pickle.load(open(f'{working_dir}/saved_models/aids_model.sav', 'rb'))
#Done covid 
covid_model = pickle.load(open(f'{working_dir}/saved_models/covid_model.sav', 'rb'))
#Done Asthma
asthma_model = pickle.load(open(f'{working_dir}/saved_models/asthma_model.sav', 'rb'))
 
cKidney_model = pickle.load(open(f'{working_dir}/saved_models/cKidney_model.sav', 'rb'))
#Done Parkinsons
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
#Done Dengue
Dengue_model = pickle.load(open(f'{working_dir}/saved_models/dengue_model.sav', 'rb'))
# ----------------- CSV Database Setup -----------------
USER_DB_FILE = "users.csv"

BACKGROUND_IMAGES = {
    "Heart Diseases": "Images/heart1.png",
    "Hypertension": "Images/hypertension1.jpg",
    "Stroke": "Images/stroke.jpg",
    "Heart Failure": "Images/heart failure1.jpg",

    "Diabetes": "Images/diabetes1.jpg",
    "Thyroid Disorders": "Images/thyroid1.jpg",
    "Obesity & Metabolic Syndrome": "Images/obesity1.jpg",

    # "Brain Tumor": "Images/brain tumor.jpg",
    "Parkinson's Disease": "Images/parkison's1.jpg",
    "Migraine & Chronic Headaches": "Images/Migraine_Chronic_Headaches1.jpg",
    "Sleep Disorders": "Images/sleep1.jpg",

    "Asthma": "Images/asthma.jpg",
    "Lung Cancer": "Images/lung cancer1.jpg",
    "Chronic Obstructive Pulmonary Disease": "Images/Chronic Obstructive Pulmonary Disease1.jpg",
    # "Tuberculosis": "Images/Tuberculosis.jpg",

    "Chronic Kidney Disease": "Images/Chronic Kidney Disease1.jpg",
    "Kidney Stones": "Images/Kidney Stones1.jpg",
    # "Hypertensive Nephropathy": "Images/Hypertensive Nephropathy.jpg",

    "Covid-19": "Images/covid1.jpg",
    # "Influenza": "Images/Influenza.jpg",
    "HIV/AIDS": "Images/HIVAIDS1.jpg",
    # "Malaria": "Images/malaria.jpg",
    "Dengue": "Images/malaria1.jpg"
}



def load_users():
    if not os.path.exists(USER_DB_FILE):
        pd.DataFrame(columns=["username", "password"]).to_csv(USER_DB_FILE, index=False)
    return pd.read_csv(USER_DB_FILE, index_col=0).to_dict().get("password", {})

def save_users(users_dict):
    pd.DataFrame(list(users_dict.items()), columns=["username", "password"]).to_csv(USER_DB_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    df = pd.read_csv(USER_DB_FILE)

    if username in df["username"].values:
        st.error("❌ Username already exists. Please choose a different one.")
        return

    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB_FILE, index=False)

    st.session_state["registration_success"] = True
    st.success("✅ Registration successful! You can now log in.")

def check_credentials(username, password):
    df = pd.read_csv(USER_DB_FILE)
    user = df[df["username"] == username]
    return not user.empty and user["password"].values[0] == hash_password(password)

def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <style>
                    .main {{
                        background-image: url("data:image/png;base64,{encoded}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

def login():
    # set_background("Images/blur_homePage.jpeg")
    set_background("Images/backgroundlogin2.jpg")
    st.markdown("<h1 style='text-align: center; font-size: 52px;'>🔐 Login Page</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])  # Center column is wider
    st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: black !important;  / Set label color to black /
                      }
                </style>
                <style>
                      .stTextInput label {
                        font-weight: bold !important;
                        }
                       </style>
                <style>
                      .stButton label {
                        font-weight: bold !important;
                        }
                       </style>
                """,
                unsafe_allow_html=True
            )
    with col2:
        username = st.text_input("👤 User Name")
        password = st.text_input("🔑 Password", type="password")

    col4, col5, col6 = st.columns([5, 1, 2])
    with col5:
        if st.button("Login"):
            # Basic validations
            if not username or not password:
                st.warning("⚠️ Username and Password cannot be empty.")
            elif " " in username or " " in password:
                st.warning("⚠️ Username and Password should not contain spaces.")
            elif len(password) < 8:
                st.warning("⚠️ Password must be at least 8 characters long.")
            else:
                with st.spinner("🔄 Verifying credentials..."):
                    time.sleep(1)

                if check_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login Successful!...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")



def register():
 
 
#     set_background(Image.open("Images/backgroundlogin2.jpg"))
 def set_background(image_path):
  if os.path.exists(image_path):
   image = Image.open(image_path)
   st.image(image, use_column_width=True)
  else:
   st.error(f"Image not found: {image_path}")



    st.markdown("<h1 style='text-align: center; font-size: 52px;'>📝 Register New Account</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])  # Center column is wider
    st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: black !important;  / Set label color to black /
                      }
                </style>
                <style>
                      .stTextInput label {
                        font-weight: bold !important;
                        }
                       </style>
                <style>
                      .stButton label {
                        font-weight: bold !important;
                        }
                       </style>
                """,
                unsafe_allow_html=True
            )
    with col2:
        new_username = st.text_input("👤 Choose a User Name")
        new_password = st.text_input("🔑 Choose a Password", type="password")

    col4, col5, col6 = st.columns([5, 1, 2])
    with col5:
        if st.button("Register"):
            if not new_username or not new_password:
                st.warning("⚠️ Username and Password cannot be empty.")
            elif " " in new_username or " " in new_password:
                st.warning("⚠️ Username and Password should not contain spaces.")
            elif len(new_password) < 8:
                st.warning("⚠️ Password must be at least 8 characters long.")
            else:
                register_user(new_username, new_password)
                # st.success("✅ Registration successful! You can now log in.")
                time.sleep(2)
                st.session_state["page"] = "Login"
                st.rerun()

def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.success("✅ Logged out successfully!")
    st.rerun()



def set_background_color(color):
    st.markdown(
        f"""
        <style>
            .main {{
                background-color: {color};  / Set background color /
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def home_page():
    # set_background("Images/background_Final.jpg")
    # set_background("Images/blur_homePage.jpeg")
    set_background("Images/backgroundlogin2.jpg")
    set_background_color("#f8f9fa")  # Apply light blue background color for the home page
    st.markdown(
    """
    <h1 style="text-align:; color: #000; text-shadow: 2px 2px 5px white;">🌟 Welcome to Dr. D&R Health Analyzer—Your Key to a Healthier You!</h1>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p><strong>Dr. D&R Health Analyzer, dreamed up by the brilliant Doctor Dhrushi and Roshni, is your friendly guide to staying healthy and happy!
        Powered by smart AI, this platform makes understanding your health fun, simple, and empowering. 
        Whether you’re curious about your wellness or a healthcare pro looking for answers, Dr. D&R is here to light the way with clear, personalized insights that spark confidence and joy.</strong> </p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <h1 style="text-align:; color: #000; text-shadow: 2px 2px 5px white;">🌈 What Makes Dr. D&R So Special?</h1>
    """,
    unsafe_allow_html=True
)

    # st.title("🌈 What Makes Dr. D&R So Special?")
    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p><strong>Imagine a tool that feels like a caring friend, always ready to help you stay one step ahead of health concerns.
        Dr. D&R uses cutting-edge machine learning to check for risks in all sorts of areas—like your heart, blood sugar, brain, lungs, kidneys, and liver. 
        It’s like having a health superhero watching over you! 
        With its bright, easy-to-use design, exploring your health feels like a breeze, whether you’re at home or in a clinic. 
        Complex medical stuff? Dr. D&R turns it into colorful, clear tips that make sense and inspire you to take charge.</strong> </p>
    </div>
    """,
    unsafe_allow_html=True
)
    st.markdown(
    """
    <h1 style="text-align:; color: #000; text-shadow: 2px 2px 5px white;">🚀 How It Works—Simple Steps to Wellness!</h1>
    """,
    unsafe_allow_html=True
)

    # st.title("🚀 How It Works—Simple Steps to Wellness!")

    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p><strong>Join the Fun: Sign up and log in to Dr. D&R's safe, welcoming platform — it's super easy to get started!</strong></p>
        <p><strong>Share Your Info: Want to know if you're at risk for something? Just enter your health details, and Dr. D&R will do the rest.</strong></p>
        <p><strong>See the Results: Get a quick, clear answer about whether you might have a condition, backed by smart tech you can trust.</strong></p>
    </div>
    """,
    unsafe_allow_html=True
)


#     st.write(
#     "**Join the Fun: Sign up and log in to Dr. D&R's safe, welcoming platform — it's super easy to get started!** "
#     "**Share Your Info: Want to know if you're at risk for something? Just enter your health details, and Dr. D&R will do the rest.** "
#     "**See the Results: Get a quick, clear answer about whether you might have a condition, backed by smart tech you can trust.**"
# )
    st.markdown(
    """
    <h1 style="text-align:; color: #000; text-shadow: 2px 2px 5px white;">Get Your Plan:</h1>
    """,
    unsafe_allow_html=True
)
    # st.title("Get Your Plan:")
    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p><strong>If There’s a Risk: You’ll get friendly, tailored tips to manage or prevent it—like small lifestyle changes or care ideas.</strong></p>
        <p><strong>If You’re All Clear: Discover simple ways to keep feeling great and stay healthy for the long haul.</strong></p>
        <p><strong>Enjoy the Journey: With a lively, intuitive dashboard, understanding your health is exciting and empowering every step of the way.</strong></p>
  
    </div><br><br>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p>✅ <strong>Checks Lots of Conditions: From heart health to lung care, it’s got you covered with comprehensive insights.</strong></p>
        <p>😊 <strong>Fun & Friendly: Its cheerful design makes health feel approachable for everyone—no matter who you are.</strong></p>
        <p>🎯 <strong>Personalized Just for You: Get advice that fits your life, helping you make choices that keep you glowing.</strong></p>
        <p>🤖 <strong>Trustworthy & Smart: Built with the latest AI, Dr. D&R grows with you, offering reliable guidance you can count on.</strong></p>
    </div><br><br>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    """
    <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
        <p><strong>With Dr. D&R, health isn’t a chore—it’s a joyful adventure! Sign up today, take the first step, and let us guide you to a brighter, healthier future filled with confidence and vitality.</strong></p>
        <p><strong>Join the Dr. D&R family and make wellness your happy place!</strong></p>
    </div><br><br>
    """,
    unsafe_allow_html=True
)




def create_pdf(disease_name, user_inputs, diagnosis):
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Title of the PDF
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f'{disease_name} Prediction Report', ln=True, align='C')
 
    # Add user inputs to PDF
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, '', ln=True)
    for field, value in user_inputs.items():
        pdf.cell(200, 10, f'{field} :- {value}', ln=True)
    # Add prediction result to PDF
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, f'Prediction: {diagnosis}', ln=True)
    # Save PDF to file
    pdf_output_path = os.path.join(working_dir, 'prediction_report.pdf')
    pdf.output(pdf_output_path)
 
    return pdf_output_path




def about_us():
    set_background("Images/backgroundlogin2.jpg")
    st.markdown(
    """
    <h1 style="text-align:; color: #000; text-shadow: 2px 2px 5px white;">👩‍⚕️ About Us – Dr. D&R</h1>
    """,
    unsafe_allow_html=True
)
    # st.title("👩‍⚕️ About Us – Dr. D&R")

    # About Dr. Dhrushi and Dr. Roshni
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.image("Images/dhrushi3.jpg", caption="Dr. Dhrushi", width=200)
        
        st.markdown(
        """
        <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
            <st.image src="Images/dhrushi3.jpg" caption="Dr. Dhrushi" width="200" />
            <p><strong>Dr. Dhrushi Kapadiya</strong></p>
            <p><strong>🩺 <em>Specialization:</em> Cardiologist, Data-driven Healthcare Researcher</strong></p>
            <p><strong>🎓 <em>Education:</em> MBBS, MD from Charusat Medical College</strong></p>
            <p><strong>📆 <em>Experience:</em> 10+ years in clinical practice and AI-powered diagnostics</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    with col2:
        st.image("Images/roshni5.jpeg", caption="Dr. Roshni", width=200)
        st.markdown(
        """
        <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
            <st.image src="Images/roshni1.jpeg" caption="Dr. Roshni" width="200" />
            <p><strong>Dr. Roshni Khatri</strong></p>
            <p><strong>🩺 <em>Specialization:</em> Endocrinologist, AI-driven Health Specialist</strong></p>
            <p><strong>🎓 <em>Education:</em> MBBS, MD from Charusat University</strong></p>
            <p><strong>📆 <em>Experience:</em> 8+ years in medical research and healthcare technology</strong></p>
        </div><br><br>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # Mission section in transparent box
    st.markdown(
        """
        <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
            <p><strong>🌟 Our Mission</strong></p>
            <p><strong><em>At Dr. D&R Health Analyzer, we’re passionate about making health simple and exciting! Using the power of Python and Machine Learning, we aim to catch health concerns early, so you can stay ahead with ease. Our goal is to empower everyone—whether you’re at home or a healthcare pro—with clear, helpful insights to make better choices and live vibrantly. We see health as a joyful adventure, and we’re here to guide you every step of the way to a happier, healthier you!</em></strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Health Analyzer section in transparent box
    st.markdown(
        """
        <div style="background-color: rgba(240, 240, 240, 0.5); padding: 20px; border-radius: 12px;">
            <p><strong>🚀 Dr. D&R Health Analyzer—Your Bright Path to Better Health!</strong></p>
            <p><em><strong>Say hello to Dr. D&R Health Analyzer, a wonderful creation by Doctor Dhrushi and Roshni that’s here to make staying healthy feel like a fun, uplifting adventure! This clever AI-powered tool is like a friendly companion, always ready to help you understand what’s going on with your body. It’s designed to look out for possible health concerns in all sorts of areas—like keeping your heart strong, balancing your blood sugar, caring for your brain, helping you breathe easy, and supporting your kidneys and liver. Whether you’re someone who wants to feel more confident about your wellness or a healthcare professional searching for clear answers, Dr. D&R makes it super simple and exciting. With its cheerful, easy-to-navigate design, it feels like a warm hug, turning complicated health information into bright, understandable insights that light up your journey. Just share a bit about yourself, and Dr. D&R uses its smart technology to give you personalized tips and predictions that are easy to follow. It’s all about empowering you to take small, meaningful steps toward a healthier, happier life, making wellness something you look forward to every day.<strong></em></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to generate PDF report (reusable for all diseases)
def generate_pdf_report(name, pid, diagnosis, inputs, param_names):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f" Prediction Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Patient Name: {name}", ln=True)
    if pid:
        pdf.cell(0, 10, f"Patient Phone Number: {pid}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Input Parameters:", ln=True)
    pdf.set_font("Arial", "", 12)
    for param, value in zip(param_names, inputs):
        pdf.cell(0, 8, f"{param}: {value}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Diagnosis:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, diagnosis)
    pdf.ln(10)
    return pdf.output(dest="S")


def prediction_page():
    set_background("Images/backgroundlogin2.jpg")
    st.sidebar.title("Select Category")
    menu = {
        "Cardiovascular Diseases": ["Heart Diseases", "Hypertension", "Stroke", "Heart Failure"],
        "Metabolic & Endocrine Diseases": ["Diabetes", "Thyroid Disorders", "Obesity & Metabolic Syndrome"],
        "Neurological Disorders": ["Parkinson's Disease", "Migraine & Chronic Headaches", "Sleep Disorders"],
        "Respiratory Diseases": ["Asthma", "Lung Cancer", "Chronic Obstructive Pulmonary Disease"],
        "Renal & Liver Diseases": ["Chronic Kidney Disease", "Kidney Stones"],
        "Infectious Diseases": ["Covid-19", "HIV/AIDS", "Dengue"]
    }

    main_choice = st.sidebar.selectbox("Select Category", ["Select Category"] + list(menu.keys()))

    if main_choice and main_choice != "Select Category":
        sub_choice = st.sidebar.radio("Select Disease", menu[main_choice])

        if sub_choice in BACKGROUND_IMAGES:
            set_background(BACKGROUND_IMAGES[sub_choice])
            

#Diabetes 
        if sub_choice == "Diabetes":
            st.markdown("<h3 style='color: white;'>Diabetes Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                Pregnancies=st.text_input("Pregnancies")
            with col2:
                Glucose=st.text_input("Glucose")
            with col1:
                BloodPressure=st.text_input("BloodPressure")
            with col2:
                SkinThickness=st.text_input("SkinThickness")
            with col1:
                Insulin=st.text_input("Insulin")
            with col2:
                BMI=st.text_input("Body Mass Index")
            with col1:
                DiabetesPedigreeFunction=st.text_input("Diabetes Pedigree Function")
            with col2:
                Age=st.text_input("Age")

            # Additional input for patient details
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")

                # Function to generate PDF report
            # def generate_pdf_report(name, pid, diagnosis, inputs):
            #     pdf = FPDF()  # This line requires the FPDF import
            #     pdf.add_page()
            #     pdf.set_font("Arial", "B", 16)
            #     pdf.cell(0, 10, "Diabetes Prediction Report", ln=True, align="C")
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            #     pdf.cell(0, 10, f"Patient Name: {name}", ln=True)
            #     if pid:
            #         pdf.cell(0, 10, f"patient_no: {pid}", ln=True)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     pdf.cell(0, 10, "Input Parameters:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     param_names = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
            #                    "Insulin", "BMI", "Diabetes Pedigree Function", "Age"]
            #     for param, value in zip(param_names, inputs):
            #         pdf.cell(0, 8, f"{param}: {value}", ln=True)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     pdf.cell(0, 10, "Diagnosis:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.multi_cell(0, 8, diagnosis)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     # pdf.cell(0, 10, "Suggestions:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.multi_cell(0, 8)
            #     return pdf.output(dest="S").encode("latin1")
            
            param_names = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
                           "Insulin", "Body Mass Index", "Diabetes Pedigree Function", "Age"]
            # code for Prediction
            diab_diagnosis = ''
            st.markdown("""
                        <style>
                        [data-testid="stSuccess"] > details > summary {
                        #     font-size: 250px;
                        #     font-weight: bold;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)

            if st.button('Diabetes Test Result'):

                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                    BMI, DiabetesPedigreeFunction, Age]

                user_input = [float(x) for x in user_input]

                diab_prediction = diabetes_model.predict([user_input])
                

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The Person Is Diabetic'
                    # st.success(diab_diagnosis)
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {diab_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    with st.expander("💡 Suggestions for Diabetes Management"):
                        st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                        #     font-size: 250px;
                        #     font-weight: bold;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                        st.markdown("""
                                <div style='color: white; font-size: 16px;'>
                                <b>🥗 Dietary Suggestions</b><br>
                                Eat balanced meals with:<br><br>
                                • Whole grains (brown rice, quinoa)<br>
                                • Lean proteins (fish, eggs, tofu)<br>
                                • Non-starchy vegetables (spinach, broccoli, bell peppers)<br>
                                • Healthy fats (avocados, nuts in moderation)<br><br>
                                Limit sugar and refined carbs like sweets, soda, white bread, and processed snacks.<br>
                                Control portion sizes to avoid blood sugar spikes.<br>
                                Don’t skip meals, especially breakfast—it helps stabilize blood sugar.<br>
                                Stay hydrated – drink plenty of water throughout the day.<br><br>
                        
                                <b>🏃‍♂️ Lifestyle Suggestions</b><br>
                                • Exercise regularly – even 30 minutes of walking daily helps regulate blood sugar.<br>
                                • Manage stress – try yoga, meditation, or even deep breathing.<br>
                                • Monitor blood sugar levels as advised by your doctor.<br>
                                • Get regular sleep – aim for 7–9 hours per night to support hormone balance.<br><br>
                        
                                <b>💊 Medical & Monitoring</b><br>
                                • Take medications as prescribed.<br>
                                • Regular check-ups with your healthcare provider.<br>
                                • Keep a log of blood sugar readings, meals, and symptoms.<br>
                                • Foot care – check your feet daily for cuts or blisters.<br><br>
                        
                                <b>🙅‍♂️ Avoid These</b><br>
                                • Smoking and excessive alcohol<br>
                                • Sugary drinks (replace with water or herbal teas)<br>
                                • High-sodium and high-fat processed foods
                                </div>
                                """, unsafe_allow_html=True)                
                else:

                    diab_diagnosis = 'The Person Is Not Diabetic'
                    # st.button('Suggetion For Non-Diabetes')
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {diab_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("💡 Suggestions for Diabetes Management"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px;'>
                            
                            <b>🥗 Dietary Recommendations<br>Balanced Meals</b><br>
                            • Include complex carbs (whole grains, brown rice, quinoa)<br>
                            • Pair with lean proteins and healthy fats<br>
                            • Eat plenty of non-starchy vegetables (broccoli, spinach, bell peppers)<br><br>
                        
                            <b>Limit Sugary Foods</b><br>
                            • Avoid sodas, candies, and baked goods with refined sugar<br>
                            • Watch for "hidden sugars" in processed foods and sauces<br><br>
                        
                            <b>Control Portion Sizes</b><br>
                            • Use smaller plates or measure servings if needed<br>
                            • Don't skip meals — especially breakfast<br><br>
                        
                            <b>Hydrate</b><br>
                            • Drink plenty of water (8–10 glasses/day)<br>
                            • Limit sugary drinks and alcohol<br><br>
                        
                            <b>🏃‍♂️ Lifestyle & Physical Activity</b><br>
                            <b>Stay Active</b><br>
                            • Aim for at least 150 minutes/week of moderate activity<br>
                            • Try brisk walking, swimming, cycling, or yoga<br><br>
                        
                            <b>Strength Training</b><br>
                            • 2–3 times/week can help improve insulin sensitivity<br>
                            • Bodyweight exercises (squats, pushups) or light weights<br><br>
                        
                            <b>Maintain a Healthy Weight</b><br>
                            • Even modest weight loss (5–10%) can reduce diabetes risk<br><br>
                        
                            <b>🧘‍♀️ Stress & Sleep</b><br>
                            <b>Stress Management</b><br>
                            • Chronic stress can increase blood sugar<br>
                            • Try deep breathing, meditation, journaling, or hobbies<br><br>
                        
                            <b>Quality Sleep</b><br>
                            • Aim for 7–9 hours/night<br>
                            • Avoid screens before bed; try a relaxing routine<br><br>
                        
                            <b>🩺 Monitoring & Prevention</b><br>
                            <b>Regular Checkups</b><br>
                            • Annual blood sugar tests (especially if family history or over age 40)<br>
                            • Monitor blood pressure and cholesterol<br><br>
                        
                            <b>Track Symptoms</b><br>
                            • Stay alert for fatigue, excessive thirst, or slow wound healing — early signs of blood sugar issues<br><br>
                        
                            <b>Stay Educated</b><br>
                            • Learn about diabetes risk factors, and how food and lifestyle affect health
                            
                            </div>
                            """, unsafe_allow_html=True)
                if diab_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, diab_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    # st.download_button("Download Report", data=pdf_data, file_name="report.pdf", mime="application/pdf")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Diabetes_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
                    
 #Heart                       
        if sub_choice == "Heart Diseases":
            st.markdown("<h3 style='color: white;'>Heart Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox> label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                age=st.text_input("Age")
            with col2:
                # o=[0,1]
                sex=st.selectbox("Gender",options=[ "Male", "Female"])
                sex = 0 if sex == "Female" else 1
            with col3:
                cp=st.text_input("Chest Pain")
            with col1:
                trestbps=st.text_input("Resting Blood Pressure")
            with col2:
                chol=st.text_input("Cholesterol")
            with col3:
                fbs=st.selectbox("Fasting Blood Sugar" ,options=["Yes" ,"No"])
                fbs = 0 if fbs == "No" else 1
            with col1:
                restecg=st.text_input("Resting Electrocardiographic ")
            with col2:
                thalach=st.text_input("Maximum Heart Rate Achieved During Test")
            with col3:
                # ot=[1,0]
                exang=st.selectbox("Exercise-Induced Angina",options=["Yes" ,"No"])
                exang = 0 if exang == "No" else 1
            with col1:
                oldpeak=st.text_input("Oldpeak")
            with col2:
                # op=[0,1,2]
                # slope=st.selectbox("slope(0 = upsloping,1 = flat,2 = downsloping)",op)
                label_to_value = {
                    "upsloping": 0,
                    "flat": 1,
                    "downsloping": 2
                }
                slope = st.selectbox("Slope", list(label_to_value.keys()))
                slope = label_to_value[slope]
            with col3:
                ca=st.text_input("Ca (0-3)")
            with col1:
                # o=[1,2,3]
                # thal=st.selectbox("thal (1 = normal,2 = fixed defect,3 = reversible defect)",o)
                label_to_value = {
                    "Normal": 1,
                    "Fixed defect": 2,
                    "Reversible defect": 3
                }
                thal = st.selectbox("Thalassemia", list(label_to_value.keys()))
                thal = label_to_value[thal]
            # Additional input for patient details
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age", "Sex", "Chest Pain", "Resting Blood Pressure", "Cholesterol",
                           "Fasting Blood Sugar", "Resting Electrocardiographic", 
                           "Maximum Heart Rate", "Exercise-Induced Angina", "Oldpeak",
                           "Slope", "CA", "Thalassemia"]

            heart_diagnosis = ''

            if st.button('Heart Disease Test Result'):

                user_input = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]

                user_input = [float(x) for x in user_input]

                heart_prediction = heart_model.predict([user_input])

                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The Person Has Heart Disease'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {heart_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("❤️ Heart Disease: Lifestyle & Health Tips"):
                            st.markdown("""
                            
                            <div style='color: white; font-size: 16px;'>
                        
                            🥦 <b>1. Healthy Eating</b><br>
                            Adopt a Heart-Healthy Diet<br><br>
                        
                            <u>Focus on:</u><br>
                            - Fruits & vegetables (5+ servings/day)<br>
                            - Whole grains (brown rice, oats, quinoa)<br>
                            - Lean proteins (fish, poultry, legumes)<br>
                            - Healthy fats (avocados, nuts, olive oil)<br><br>
                        
                            <u>Limit:</u><br>
                            - Saturated fats (red meat, butter)<br>
                            - Trans fats (fried foods, baked goods)<br>
                            - Excess salt and sugar<br><br>
                        
                            <i>DASH or Mediterranean Diet</i><br>
                            These dietary patterns are scientifically shown to support heart health.<br><br>
                        
                            🚶 <b>2. Regular Physical Activity</b><br>
                            - 150 minutes/week of moderate aerobic activity (e.g., brisk walking, cycling, dancing)<br>
                            - Add 2 days/week of muscle-strengthening activities (e.g., weight training, resistance bands)<br><br>
                        
                            🧘 <b>3. Stress Management</b><br>
                            Chronic stress increases blood pressure and heart workload<br>
                            Suggestions:<br>
                            - Meditation or deep breathing<br>
                            - Yoga or tai chi<br>
                            - Leisure activities (reading, music, nature walks)<br><br>
                        
                            😴 <b>4. Prioritize Sleep</b><br>
                            - 7–9 hours of quality sleep per night<br>
                            - Practice sleep hygiene: no late caffeine, screen-free bedtime routine, consistent sleep-wake times<br><br>
                        
                            🚭 <b>5. Quit Smoking & Limit Alcohol</b><br>
                            - Smoking significantly raises heart disease risk — quitting has immediate benefits<br>
                            - Alcohol in moderation: Men: ≤2 drinks/day, Women: ≤1 drink/day<br><br>
                        
                            🩺 <b>6. Routine Monitoring & Medical Management</b><br>
                            - Blood Pressure: Keep it under 120/80 mmHg if possible<br>
                            - Cholesterol: Monitor LDL, HDL, and triglycerides<br>
                            - Blood Sugar: Especially if diabetic or prediabetic<br>
                            - Medication Adherence: If prescribed statins, beta-blockers, etc., take them consistently<br>
                            - Regular Checkups: Annual screenings and follow-ups<br><br>
                        
                            ⚖️ <b>7. Maintain a Healthy Weight</b><br>
                            - BMI: Keep between 18.5 and 24.9<br>
                            - Waist circumference: Men < 40 inches, Women < 35 inches<br><br>
                        
                            ✅ <b>Summary for Patients</b><br>
                            Eat clean. Move daily. Breathe deeply. Sleep well. Monitor health. Quit bad habits.
                        
                            </div>
                            """, unsafe_allow_html=True)

                else:
                    heart_diagnosis = 'The Person Has Not Heart Disease'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {heart_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("💓 Non-Heart Disease Patient Tips (Heart Health Prevention Plan)"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            🥗 <b>1. Adopt a Heart-Healthy Diet</b><br>
                            <u>Focus on:</u><br>
                            - Fruits and vegetables (at least 5 servings/day)<br>
                            - Whole grains (brown rice, oats, barley)<br>
                            - Lean protein (chicken, fish, legumes)<br>
                            - Healthy fats (olive oil, nuts, seeds, avocado)<br><br>
                        
                            <u>Limit:</u><br>
                            - Processed meats, fried foods<br>
                            - Sugary drinks and snacks<br>
                            - Excess salt and saturated fats<br><br>
                        
                            📝 <i>Tip:</i> Aim for colorful meals — the more natural colors, the more nutrients!<br><br>
                        
                            🏃 <b>2. Stay Physically Active</b><br>
                            - Minimum: 150 minutes of moderate-intensity exercise/week (e.g., brisk walking, swimming, cycling)<br>
                            - Include strength training 2x/week<br>
                            - Take breaks from long sitting periods<br><br>
                        
                            🚬 <b>3. Avoid Tobacco and Minimize Alcohol</b><br>
                            - Don’t smoke – it’s the #1 preventable risk factor for heart disease<br>
                            - If you drink, do so in moderation:<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Men: ≤2 drinks/day<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Women: ≤1 drink/day<br><br>
                        
                            🧘 <b>4. Manage Stress Early</b><br>
                            - Chronic stress affects blood pressure and inflammation<br>
                            Try:<br>
                            - Meditation or mindfulness<br>
                            - Breathing exercises<br>
                            - Spending time in nature or with loved ones<br><br>
                        
                            🛌 <b>5. Prioritize Quality Sleep</b><br>
                            - 7–9 hours of uninterrupted sleep each night<br>
                            - Avoid caffeine late in the day<br>
                            - Limit screens before bedtime<br><br>
                        
                            ⚖️ <b>6. Maintain a Healthy Weight</b><br>
                            - Aim for a BMI between 18.5 and 24.9<br>
                            - Maintain a healthy waist circumference (under 40 in for men, 35 in for women)<br>
                            - Avoid crash diets — focus on long-term habits<br><br>
                        
                            🩺 <b>7. Schedule Preventive Health Screenings</b><br>
                            - Blood pressure: every 1–2 years<br>
                            - Cholesterol check: every 4–6 years, more often if at risk<br>
                            - Blood sugar: especially if overweight or family history of diabetes<br>
                            - Annual check-ups: to catch silent risk factors early<br><br>
                        
                            💧 <b>8. Hydration & Mindful Living</b><br>
                            - Drink at least 6–8 glasses of water/day<br>
                            - Reduce sugary beverages<br>
                            - Practice mindfulness — tune into how your body feels<br><br>
                        
                            ✅ <b>Quick Summary for Non-Heart Disease Patients:</b><br>
                            Live smart. Eat real. Move often. Stress less. Sleep well. Check regularly.
                        
                            </div>
                            """, unsafe_allow_html=True)
    
                if heart_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, heart_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Heart_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")

 #Hypertension complete       
        if sub_choice == "Hypertension":
            st.markdown("<h3 style='color: white;'>Hypertension Disease Prediction</h3>", unsafe_allow_html=True)
            # st.subheader("Hypertension Disease Prediction")
            # Add custom CSS for black labels in Hypertension section
            st.markdown(
                 """
                 <style>
                      .stSelectbox> label {
                      color:white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                age=st.text_input("Age")
            with col2:
                sex = st.selectbox("Select Gender:", options=["Female", "Male"])
                sex = 0 if sex == "Female" else 1
            with col1:
                label_to_value = {
                    "Typical angina": 0,
                    "Atypical angina": 1,
                    "Non-anginal pain": 2,
                    "Asymptomatic": 3
                }
                cp = st.selectbox("Chest Pain", list(label_to_value.keys()))
                cp = label_to_value[cp]
            with col2:
                trestbps=st.text_input("Resting Blood Pressure ")
            with col1:
                chol=st.text_input("Cholesterol Level")
            with col2:
                fbs=st.selectbox("Fasting Blood Sugar" ,options=["True", "False"])
                fbs = 0 if fbs == "False" else 1
            with col1:
                o=[0,1]
                restecg=st.selectbox("Resting Electrocardiographic",o)
            with col2:
                thalach=st.text_input("Maximum Heart Rate")
            with col1:
                # o=[0,1]
                exang=st.selectbox("Exercise-Induced Angina",options=["Yes", "No"])
                exang = 0 if exang == "No" else 1
            with col2:
                oldpeak=st.text_input("oldpeak")
            with col1:
                # o=[0,1,2]
                # slope=st.selectbox("slope  (0 = upsloping,1 = flat,2 = downsloping)",o)
                label_to_value = {
                    "Upsloping": 0,
                    "Flat": 1,
                    "Downsloping": 2,
                }
                slope = st.selectbox("Slope", list(label_to_value.keys()))
                slope = label_to_value[slope]
            with col2:
                ca=st.text_input("Ca  (0-3)")
            with col1:
                # o=[1,2,3]
                # thal=st.selectbox("Thalassemia  (1 = normal,2 = fixed defect,3 = reversible defect)",o)
                label_to_value = {
                    "Normal": 1,
                    "Fixed defect": 2,
                    "Reversible defect": 3,
                }
                thal = st.selectbox("Thalassemia", list(label_to_value.keys()))
                thal = label_to_value[thal]
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age", "Sex", "Chest Pain", "Resting Blood Pressure", "Cholesterol",
                           "Fasting Blood Sugar", "Resting Electrocardiographic", 
                           "Maximum Heart Rate", "Exercise-Induced Angina", "Oldpeak",
                           "Slope", "CA", "Thalassemia"]            
            hyp_diagnosis = ''

            if st.button('Hypertension Test Result'):

                user_input = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]

                user_input = [float(x) for x in user_input]

                hyp_prediction = hyp_model.predict([user_input])

                if hyp_prediction[0] == 1:
                    hyp_diagnosis = 'The Person Has Hypertension'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {hyp_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🔴 Hypertension (High Blood Pressure) Management Tips"):
                            st.markdown("""
                            <div style='color: #f8f8ff; font-size: 16px; line-height: 1.6;'>
                        
                            🥗 <b>1. Follow the DASH Diet</b><br>
                            <i>DASH = Dietary Approaches to Stop Hypertension</i><br><br>
                        
                            <u>Eat:</u><br>
                            🌿 Vegetables & 🥭 fruits (4–5 servings/day)<br>
                            🥣 Whole grains<br>
                            🥛 Low-fat dairy<br>
                            🥜 Nuts, seeds, legumes<br><br>
                        
                            <u>Limit:</u><br>
                            🧂 Sodium<br>
                            🍭 Sugar<br>
                            🍟 Processed foods<br><br>
                        
                            🧂 <b>2. Reduce Sodium Intake</b><br>
                            - Aim for &lt; 1,500–2,300 mg/day<br>
                            - Read food labels<br>
                            - Avoid canned, packaged, and restaurant foods<br>
                            - Use herbs/spices instead of salt for flavor<br><br>
                            🧠 <i>Tip:</i> “Salt hides in processed food, not just your shaker.”<br><br>
                        
                            🏃‍♂️ <b>3. Exercise Regularly</b><br>
                            - Goal: 150 min/week of moderate-intensity activity (e.g., brisk walking)<br>
                            - Add strength training 2× per week<br>
                            - 📉 Regular activity can lower BP by 5–8 mmHg!<br><br>
                        
                            ⚖️ <b>4. Achieve or Maintain a Healthy Weight</b><br>
                            - Losing even 5–10% of body weight can significantly lower BP<br>
                            - Focus on gradual, sustainable weight loss<br><br>
                        
                            🚭 <b>5. Quit Smoking</b><br>
                            - Each cigarette causes a temporary spike in BP<br>
                            - Long-term smoking damages arteries, increasing hypertension risk<br><br>
                        
                            🍷 <b>6. Limit Alcohol</b><br>
                            - Moderate intake:<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Men: up to 2 drinks/day<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Women: up to 1 drink/day<br>
                            - Heavy drinking raises blood pressure<br><br>
                        
                            😌 <b>7. Manage Stress</b><br>
                            Try:<br>
                            - Deep breathing or meditation 🧘<br>
                            - Journaling ✍️<br>
                            - Mindfulness & therapy<br>
                            - Chronic stress hormones (like cortisol) raise BP<br><br>
                        
                            🛌 <b>8. Get Enough Quality Sleep</b><br>
                            - Aim for 7–9 hours/night<br>
                            - Poor sleep is linked to higher blood pressure<br>
                            - Treat any underlying sleep apnea if present<br><br>
                        
                            🩺 <b>9. Take Medications as Prescribed</b><br>
                            - Never skip doses<br>
                            - Work with your doctor to find the right combo<br>
                            - Monitor BP at home 📉<br><br>
                        
                            🧬 <b>10. Understand Risk Factors</b><br>
                            - Family history, age, diabetes, and kidney disease may affect your BP<br>
                            - Regular checkups help detect and treat early<br><br>
                        
                            ✅ <b>Daily Summary Checklist</b><br>
                            ✅ Eat low-sodium foods<br>
                            ✅ Move your body daily<br>
                            ✅ Avoid smoking & alcohol<br>
                            ✅ Reduce stress<br>
                            ✅ Get good sleep<br>
                            ✅ Track your blood pressure<br>
                            ✅ Take your meds if prescribed<br>
                        
                            </div>
                            """, unsafe_allow_html=True)

                else:
                    hyp_diagnosis = 'The Person Has Not Hypertension'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {hyp_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🛡️ Non-Hypertensive Patient Recommendations (For Prevention & Long-Term Heart Health)"):
                                st.markdown("""
                                <div style='color: #f8f8ff ; font-size: 16px; line-height: 1.6;'>
                            
                                <strong>🥦 <b>1. Continue a Balanced, Heart-Healthy Diet</b><br>
                                Focus on:<br>
                                - Fresh fruits 🍎 and vegetables 🥬<br>
                                - Whole grains 🌾<br>
                                - Lean proteins like fish 🐟, legumes, and nuts 🥜<br>
                                - Keep sodium and saturated fat intake in check<br>
                                - Avoid excessive processed or salty snacks<br><br>
                            
                                🧘‍♀️ <b>2. Stay Physically Active</b><br>
                                At least 150 minutes/week of moderate exercise:<br>
                                - Walking 🚶‍♂️<br>
                                - Cycling 🚴‍♀️<br>
                                - Swimming 🏊<br>
                                Physical activity supports healthy blood pressure and cardiovascular strength<br><br>
                            
                                🧂 <b>3. Maintain Low Sodium Habits</b><br>
                                Even with normal BP, it’s wise to avoid too much salt<br>
                                - Read labels and opt for low-sodium alternatives<br><br>
                            
                                🚭 <b>4. Avoid Smoking or Vaping</b><br>
                                - Smoking can slowly damage blood vessels and increase future BP risk<br>
                                - If you don’t smoke — great! Stay smoke-free 🚫🚬<br><br>
                            
                                ⚖️ <b>5. Maintain a Healthy Weight</b><br>
                                - Staying within a healthy BMI range helps reduce stress on the heart<br>
                                - Avoid rapid weight gain from high-calorie, low-nutrient foods<br><br>
                            
                                💤 <b>6. Prioritize Quality Sleep</b><br>
                                - Aim for 7–9 hours/night<br>
                                - Poor sleep is linked to long-term BP increases and heart disease<br><br>
                            
                                🍷 <b>7. Keep Alcohol Intake Moderate</b><br>
                                Occasional drinking is okay, but stick to:<br>
                                - ≤ 1 drink/day (women)<br>
                                - ≤ 2 drinks/day (men)<br>
                                - Excess alcohol raises long-term hypertension risk<br><br>
                            
                                🧠 <b>8. Manage Stress Effectively</b><br>
                                Use stress-reduction techniques regularly:<br>
                                - Meditation<br>
                                - Journaling 📓<br>
                                - Deep breathing or nature walks 🌳<br><br>
                            
                                💉 <b>9. Get Regular Health Checkups</b><br>
                                - Annual blood pressure monitoring is recommended, even for healthy individuals<br>
                                - Early detection = better prevention<br><br>
                            
                                📵 <b>10. Limit Caffeine & Energy Drinks</b><br>
                                - For sensitive individuals, excess caffeine may raise BP<br>
                                - Stay hydrated with water 💧 instead of sugary or high-caffeine drinks<br><br>

                                </strong>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if hyp_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, hyp_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Hypertension_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")                
            

#Stroke
        if sub_choice == "Stroke":
            st.markdown("<h3 style='color: white;'>Stroke Disease Prediction</h3>", unsafe_allow_html=True)
            # Add custom CSS for black labels in Hypertension section
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            # getting the input data from the user
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sex = st.selectbox("Gender", options=["Female", "Male"])
                sex = 0 if sex == "Female" else 1

            with col2:
                age = st.text_input('Age')

            with col3: 
                # opt=[0,1]
                hypertension = st.selectbox("Hypertension"  ,options=["Yes", "No"])
                hypertension = 0 if hypertension == "No" else 1

            with col1:
                # opt=[0,1]
                heart_disease = st.selectbox("Heart Disease" , options=["Yes", "No"])
                heart_disease = 0 if heart_disease == "No" else 1

            with col2:
                # opt=[0,1]
                ever_married = st.selectbox("Ever Married",  options=["Yes", "No"])
                ever_married = 0 if ever_married == "No" else 1

            with col3:
                # o=[0,1,2,3,4]
                # work_type = st.selectbox('Work_type  (0 = children 1 = Govt job 2 =Never worked 3 = Private 4 = Self-employed)',o)

                label_to_value = {
                    "Children": 0,
                    "Govt job": 1,
                    "Never worked" : 2,
                    "Private" : 3,
                    "Self-employed" : 4
                }
                work_type = st.selectbox("Work Type", list(label_to_value.keys()))
                work_type = label_to_value[work_type]

            with col1:
                # o=[0,1]
                Residence_type = st.selectbox('Residence Type' , options=["Rural", "Urban"])
                Residence_type = 0 if Residence_type == "Rural" else 1

            with col2:
                avg_glucose_level = st.text_input('Avg Glucose Level')

            with col3:
                bmi = st.text_input('Body Mass Index')

            with col1:
                # o=[1,0]
                smoking_status = st.selectbox('Smoking Status' , options=["Yes", "No"])
                smoking_status = 0 if smoking_status == "No" else 1
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Gender", "Age", "Hypertension", "Heart disease","Ever married","Work Type","Residence Type",
                           "Avg glucose level","Body Mass Index","Smoking Status"]            

            stroke_diagnosis = ''

            if st.button('Stroke Disease Test Result'):

                user_input = [sex,age,hypertension,heart_disease,ever_married,
                                                   work_type,Residence_type,avg_glucose_level,bmi,smoking_status]

                # user_input = [float(x) for x in user_input]
                # scaler_input=scaler.fit_transform(user_input)

                stroke_prediction = stroke_model.predict(scaler.fit_transform([user_input]))
                

                if stroke_prediction[0] == 1:
                    stroke_diagnosis = 'The Person Has Stroke Disease'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {stroke_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧠 Stroke Prevention & Management Recommendations"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                                <strong>
                            
                                🥦 <b>1. Adopt a Brain-Healthy Diet</b><br>
                                Emphasize:<br>
                                - Leafy greens (spinach, kale) 🥬<br>
                                - Berries, citrus fruits 🍊<br>
                                - Whole grains, legumes, and nuts 🥜<br>
                                - Omega-3 rich fish (salmon, sardines) 🐟<br>
                                Limit:<br>
                                - Trans fats, saturated fats<br>
                                - Sugary snacks, red/processed meats<br>
                                - Excess salt (aim &lt;1500mg sodium/day)<br><br>
                            
                                🧘‍♂️ <b>2. Control Blood Pressure</b><br>
                                - High BP is the #1 risk factor for stroke<br>
                                - Monitor regularly<br>
                                - Reduce salt, stress, and alcohol<br>
                                - If prescribed, take antihypertensive meds consistently<br><br>
                            
                                🚭 <b>3. Stop Smoking Immediately</b><br>
                                - Smoking damages blood vessels and doubles stroke risk<br>
                                - Quitting has almost immediate benefits on blood flow and pressure<br><br>
                            
                                🚶 <b>4. Stay Physically Active</b><br>
                                At least 30 minutes/day, 5 days/week:<br>
                                - Walking, yoga, swimming, tai chi<br>
                                - Regular movement improves blood flow to the brain and reduces clot risk<br><br>
                            
                                💤 <b>5. Prioritize Sleep Health</b><br>
                                - Poor sleep or sleep apnea can increase stroke risk<br>
                                - Aim for 7–9 hours of restful sleep per night<br>
                                - Get evaluated for sleep disorders if needed<br><br>
                            
                                ⚖️ <b>6. Maintain a Healthy Weight</b><br>
                                - Obesity is linked to high BP, diabetes, and stroke<br>
                                - Losing even 5–10% of body weight can reduce risk significantly<br><br>
                            
                                💉 <b>7. Manage Chronic Conditions</b><br>
                                - <b>Diabetes:</b> Control blood sugar (HbA1c &lt;7%)<br>
                                - <b>Cholesterol:</b> Monitor LDL/HDL, eat low-fat diet<br>
                                - <b>Atrial Fibrillation (AFib):</b> Can cause blood clots — follow treatment closely<br><br>
                            
                                🍷 <b>8. Limit Alcohol Consumption</b><br>
                                - If drinking, do so in moderation:<br>
                                - ≤1 drink/day for women<br>
                                - ≤2 drinks/day for men<br>
                                - Heavy drinking increases BP and stroke risk<br><br>
                            
                                🧠 <b>9. Be Aware of Stroke Symptoms</b><br>
                                <b>FAST acronym:</b><br>
                                - Face drooping<br>
                                - Arm weakness<br>
                                - Speech difficulty<br>
                                - Time to call emergency 🚨<br>
                                - Educate family/caregivers too<br><br>
                            
                                🧠 <b>10. Take Prescribed Medications</b><br>
                                - Blood thinners (e.g., aspirin, warfarin)<br>
                                - BP medications<br>
                                - Cholesterol-lowering meds (e.g., statins)<br>
                                - Never skip or change dose without doctor consultation<br><br>
                                </strong>
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    stroke_diagnosis = 'The Person Have Not Stroke Disease'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {stroke_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧠 Non-Stroke Individuals – Preventive Health Tips"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                💪 <b>1. Keep Blood Pressure in Check</b><br>
                                Target: &lt;120/80 mmHg<br>
                                - Reduce sodium, avoid processed foods<br>
                                - Stay physically active and manage stress<br><br>
                            
                                🩺 <b>2. Get Regular Health Screenings</b><br>
                                Monitor:<br>
                                - Blood pressure<br>
                                - Blood sugar (to prevent diabetes)<br>
                                - Cholesterol (LDL, HDL)<br>
                                <i>Early detection = better prevention</i><br><br>
                            
                                🍎 <b>3. Follow a Brain-Friendly Diet</b><br>
                                Embrace:<br>
                                - DASH or Mediterranean diet<br>
                                - Leafy greens, whole grains, fruits, legumes<br>
                                - Healthy fats (olive oil, nuts, avocado)<br>
                                Limit:<br>
                                - Fried foods, sugar, processed meats<br><br>
                            
                                🚭 <b>4. Avoid Smoking & Secondhand Smoke</b><br>
                                - Smoking damages blood vessels and increases stroke risk over time<br>
                                - Quitting improves heart and brain health quickly<br><br>
                            
                                🏃 <b>5. Stay Active</b><br>
                                - At least 150 minutes of moderate exercise/week<br>
                                - Brisk walking, swimming, dancing, cycling<br>
                                - Improves circulation and maintains healthy weight<br><br>
                            
                                😴 <b>6. Prioritize Sleep Quality</b><br>
                                - Aim for 7–9 hours/night<br>
                                - Sleep apnea is a hidden risk factor for stroke — get screened if you snore or wake up tired<br><br>
                            
                                🍷 <b>7. Limit Alcohol Intake</b><br>
                                - Drink in moderation, if at all:<br>
                                - ≤1 drink/day (women)<br>
                                - ≤2 drinks/day (men)<br><br>
                            
                                🧘 <b>8. Manage Stress</b><br>
                                - Chronic stress raises BP and weakens immunity<br>
                                Try:<br>
                                - Meditation or yoga<br>
                                - Breathing exercises<br>
                                - Hobbies that bring calm<br><br>
                            
                                🧬 <b>9. Know Your Family History</b><br>
                                - If stroke or heart disease runs in your family:<br>
                                - Discuss preventive screenings with your doctor early<br>
                                - Lifestyle habits can offset many genetic risks<br><br>
                            
                                💊 <b>10. Take Medications Only as Needed</b><br>
                                - Avoid self-medicating<br>
                                - Only take aspirin or blood thinners if prescribed<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)
                if stroke_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, stroke_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Stroke_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
                    

            

#Migraine
        if sub_choice == "Migraine & Chronic Headaches":
            st.markdown("<h3 style='color: white;'>Migraine & Chronic Headaches Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                Age=st.text_input("Age")
            with col1:
                Duration=st.text_input("Duration of migraine attack (in hours)")
            with col1:
                Frequency=st.text_input("Frequency of migraine episodes  (times per month or week)")
            with col1:
                Location=st.selectbox("Headache location",options=["unilateral", "bilateral"])
                Location = 1 if Location == "unilateral" else 2
            with col1:
                Character=st.selectbox("Pain character",options=["throbbing", "pressing"])
                Character = 1 if Character == "throbbing" else 2
            with col1:
                Intensity=st.text_input("Intensity of pain  (1-3)")
            with col1:
                Nausea=st.selectbox("Presence of nausea during migraine",options=["Yes", "No"])
                Nausea = 0 if Nausea == "No" else 1
            with col1:
                Vomit=st.selectbox("Vomiting during migraine",options=["Yes", "No"])
                Vomit = 0 if Vomit == "No" else 1
            with col1:
                Phonophobia=st.selectbox("Sensitivity to sound",options=["Yes", "No"])
                Phonophobia = 0 if Phonophobia == "No" else 1
            with col1:
                Photophobia=st.selectbox("Sensitivity to light",options=["Yes", "No"])
                Photophobia = 0 if Photophobia == "No" else 1
            with col1:
                label_to_value = {
                    "flashing lights": 1,
                    "zigzag lines": 2,
                    "Black": 3
                }
                Visual = st.selectbox("Presence of visual aura symptoms", list(label_to_value.keys()))
                Visual = label_to_value[Visual]
            with col1:
                Sensory=st.text_input("Presence of sensory aura symptoms")
            with col1:
                Dysphasia=st.selectbox("Trouble speaking",options=["Yes", "No"])
                Dysphasia = 0 if Dysphasia == "No" else 1
            with col1:
                Dysarthria=st.selectbox("unclear speech",options=["Yes", "No"])
                Dysarthria = 0 if Dysarthria == "No" else 1
            with col1:
                Vertigo=st.selectbox("Dizziness",options=["Yes", "No"])
                Vertigo = 0 if Vertigo == "No" else 1
            with col1:
                Tinnitus=st.selectbox("Ringing in the ears",options=["Yes", "No"])
                Tinnitus = 0 if Tinnitus == "No" else 1
            with col1:
                Hypoacusis=st.selectbox("Decreased hearing ability",options=["Yes", "No"])
                Hypoacusis = 0 if Hypoacusis == "No" else 1
            with col1:
                Diplopia=st.selectbox("Double vision",options=["Yes", "No"])
                Diplopia = 0 if Diplopia == "No" else 1
            with col1:
                Defect=st.selectbox("Visual field defect",options=["Yes", "No"])
                Defect = 0 if Defect == "No" else 1
            with col1:
                Ataxia=st.selectbox("coordination",options=["Yes", "No"])
                Ataxia = 0 if Ataxia == "No" else 1
            with col1:
                Conscience=st.selectbox("confusion",options=["Yes", "No"])
                Conscience = 0 if Conscience == "No" else 1
            with col1:
                Paresthesia=st.selectbox("Abnormal sensations",options=["Yes", "No"])
                Paresthesia = 0 if Paresthesia == "No" else 1
            with col1:
                DPF =st.text_input("Disability Profile Factor  (0-1)")
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
            # def generate_pdf_report(name, pid, diagnosis, inputs):
            #     pdf = FPDF()  # This line requires the FPDF import
            #     pdf.add_page()
            #     pdf.set_font("Arial", "B", 16)
            #     pdf.cell(0, 10, "Migraine Prediction Report", ln=True, align="C")
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            #     pdf.cell(0, 10, f"Patient Name: {name}", ln=True)
            #     if pid:
            #         pdf.cell(0, 10, f"patient_no: {pid}", ln=True)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     pdf.cell(0, 10, "Input Parameters:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     param_names = ["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", 
            #                    "Insulin", "BMI", "Diabetes Pedigree Function", "Age"]
            #     for param, value in zip(param_names, inputs):
            #         pdf.cell(0, 8, f"{param}: {value}", ln=True)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     pdf.cell(0, 10, "Diagnosis:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.multi_cell(0, 8, diagnosis)
            #     pdf.ln(10)
            #     pdf.set_font("Arial", "B", 12)
            #     # pdf.cell(0, 10, "Suggestions:", ln=True)
            #     pdf.set_font("Arial", "", 12)
            #     pdf.multi_cell(0, 8)
            #     return pdf.output(dest="S").encode("latin1")
            param_names = ["Age","Duration of migraine attack (in hours)","Frequency of migraine episodes  (times per month or week)",
                           "Headache location","Pain character","Intensity of pain  (1-3)","Presence of nausea during migraine",
                           "Vomiting during migraine","Sensitivity to sound","Sensitivity to light","Presence of visual aura symptoms",
                           "Presence of sensory aura symptoms","Trouble speaking","unclear speech","Dizziness","Ringing in the ears",
                           "Decreased hearing ability","Double vision","Visual field defect","coordination","confusion","Abnormal sensations"
                           ,"Disability Profile Factor  (0-1)"]

            # code for Prediction
            migraine_diagnosis = ''

            if st.button('Migraine & Chronic Headaches Test Result'):

                input_data =[[Age,Duration,Frequency,Location,Character,Intensity,Nausea,Vomit,Phonophobia,Photophobia,
                             Visual,Sensory,Dysphasia,Dysarthria,Vertigo,Tinnitus,Hypoacusis,Diplopia,Defect,Ataxia,Conscience,Paresthesia,DPF]]
                    
                prediction = migraine_model.predict(input_data)

                migraine_diagnosis = "You have",prediction[0]
              
            st.success(migraine_diagnosis)
            if "Typical aura with migraine" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Typical Aura with Migraine – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            This common migraine type includes visual or sensory aura before headache onset. Managing triggers and prompt treatment are key.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • 💊 Use prescribed triptans or NSAIDs during migraine attacks<br>
                            • 💉 Preventive meds like beta-blockers or antiepileptics may help<br>
                            • 🧪 Regular check-ups to monitor treatment response<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🚫 Avoid triggers like chocolate, red wine, aged cheese<br>
                            • 🧂 Eat at regular intervals to prevent hunger-triggered attacks<br>
                            • 💧 Stay well-hydrated throughout the day<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🧘‍♀️ Try low-impact exercises (yoga, walking) to reduce stress<br>
                            • ⛹️ Avoid intense workouts during or right after an aura<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 🧘 Practice relaxation techniques like meditation and breathing<br>
                            • 🧠 Consider cognitive behavioral therapy (CBT) for stress management<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 🛌 Maintain a consistent sleep schedule<br>
                            • 🕶️ Wear sunglasses or use blue light filters for photophobia<br>
                            • 📓 Keep a migraine diary to identify patterns and triggers<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)



            elif "Migraine without aura" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                
                with st.expander("🧠 Migraine Without Aura – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These suggestions are aimed at managing symptoms and reducing the frequency of migraine attacks without aura.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • 💊 Use abortive treatments early in the migraine<br>
                            • 📆 Consider preventive therapy for frequent attacks<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • ⏰ Avoid skipping meals; keep a consistent eating schedule<br>
                            • ☕ Limit caffeine and alcohol intake<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🚶 Regular moderate exercise can reduce frequency<br>
                            • ❗ Avoid activity during an attack to prevent worsening symptoms<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 💆 Try biofeedback or acupuncture<br>
                            • 🧘‍♂️ Mindfulness-based stress reduction is effective<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 💡 Avoid bright lights and loud noises during migraines<br>
                            • 🛀 Take warm showers or use cold packs for relief<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)




            elif "Familial hemiplegic migraine" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Familial Hemiplegic Migraine – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These suggestions aim to help individuals with Familial Hemiplegic Migraine manage symptoms and reduce triggers.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • ❌ Avoid vasoconstrictive meds (e.g., triptans, ergotamines)<br>
                            • 💊 Use calcium channel blockers or antiepileptic drugs preventively<br>
                            • 🧬 Genetic counseling may be helpful for families<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🍽️ Maintain a migraine-safe diet; avoid MSG and nitrates<br>
                            • 💧 Stay hydrated and well-nourished<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🧘‍♂️ Gentle movement and stretching recommended<br>
                            • ❌ Avoid strenuous exercise that might trigger symptoms<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 🧠 Therapy to cope with anxiety around paralysis episodes<br>
                            • 🎧 Sound therapy or nature sounds for relaxation<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 🛏️ Prioritize rest and reduce screen time during recovery<br>
                            • 📘 Educate family on emergency symptoms and response<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)



            elif "Typical aura without migraine" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Typical Aura Without Migraine – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            This type features visual or sensory aura without the follow-up headache. Monitoring and minimizing triggers can help reduce frequency.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • 💊 May not require migraine meds unless symptoms are frequent<br>
                            • 🔄 Monitor for evolution into full migraine<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🍵 Avoid stimulants and processed foods<br>
                            • 🥦 Eat anti-inflammatory foods (greens, berries, fish)<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🧍 Gentle daily movement to support circulation<br>
                            • 🚶 Short walks can reduce visual stress triggers<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 👁️ Eye relaxation techniques (palming, 20-20-20 rule)<br>
                            • 🧘 Meditation to reduce frequency of aura episodes<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 🌗 Dim lighting and calm environment during aura<br>
                            • 📈 Track frequency and duration of aura for doctor visits<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)




            elif "Basilar-type aura" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Basilar-Type Aura – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These suggestions aim to support well-being, manage symptoms, and minimize triggers for individuals with Basilar-Type Aura.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • ⚠️ Avoid vasoconstrictors (e.g., triptans, ergotamines)<br>
                            • 💊 Use anti-nausea and preventive medications (e.g., flunarizine)<br>
                            • 🧠 Neurological monitoring for stroke-like symptoms<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🍎 Eat whole, fresh foods to reduce inflammation<br>
                            • 💧 Stay hydrated and avoid sugar crashes<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 👣 Gentle movement; avoid high altitudes or rapid exertion<br>
                            • 🚶 Consistency over intensity<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 💆 Use neck and shoulder massage for tension<br>
                            • 🧘‍♀️ Guided meditation and calming audio apps<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 🛌 Rest in a dark, quiet room during an aura<br>
                            • ❗ Educate support network on signs of worsening symptoms<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)



            elif "Other" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Other Migraine Variants – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These suggestions apply to less common migraine types such as vestibular, retinal, or other atypical presentations.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • 💊 Tailor treatment based on specific symptoms (e.g., vestibular, retinal)<br>
                            • 🧠 Neurologist referral for complex cases<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🧃 Avoid artificial sweeteners and additives<br>
                            • 🥑 Try magnesium-rich foods (avocados, nuts)<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🚶 Keep up with regular light activity<br>
                            • ⚠️ Adapt exercise routines based on dizziness or imbalance<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 🧘 Deep breathing and visualization exercises<br>
                            • 🧠 Behavioral therapy for coping with rare or disabling types<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 🕰️ Structure your day to avoid overexertion<br>
                            • 🌤️ Avoid bright lights or extreme weather if sensitive<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)



            elif "Sporadic hemiplegic migraine" in migraine_diagnosis:
                st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                with st.expander("🧠 Sporadic Hemiplegic Migraine – Wellness Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These rare migraines resemble familial hemiplegic types but occur without a family history. Proper diagnosis and careful management are key.<br><br>
                        
                            🩺 <b>Medication & Medical Care</b><br>
                            • 💊 Similar management to familial hemiplegic migraines<br>
                            • 🧪 Rule out stroke and TIA in new cases<br><br>
                        
                            🥗 <b>Diet & Nutrition</b><br>
                            • 🥗 Maintain regular meals with healthy fats and greens<br>
                            • 🧂 Avoid high-sodium and processed foods<br><br>
                        
                            🏃 <b>Exercise & Physical Activity</b><br>
                            • 🧘 Light yoga or tai chi to promote calm<br>
                            • ❌ Avoid overexertion or activities needing balance when symptoms flare<br><br>
                        
                            🧘 <b>Therapies & Stress Relief</b><br>
                            • 🧠 Cognitive therapy to manage fear or confusion during episodes<br>
                            • 🎨 Art or journaling to express emotional stress<br><br>
                        
                            🌿 <b>Lifestyle & Home Remedies</b><br>
                            • 📅 Keep a calendar of attacks to detect frequency<br>
                            • 🛌 Prioritize quality sleep and low-stress environments<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)


            user_inputs = {
                'Patient Name':patient_name,
                'Age': Age,
                'Duration of Headache (in months/years)': Duration,
                'Frequency of Headache (per month/week)': Frequency,
                'Location of Pain': Location,
                'Character of Pain': Character,
                'Intensity of Pain (scale 1-10)': Intensity,
                'Presence of Nausea': Nausea,
                'Presence of Vomiting': Vomit,
                'Phonophobia (sensitivity to sound)': Phonophobia,
                'Photophobia (sensitivity to light)': Photophobia,
                'Visual Symptoms (aura, flashes)': Visual,
                'Sensory Symptoms (tingling, numbness)': Sensory,
                'Speech Difficulties (Dysphasia)': Dysphasia,
                'Speech Difficulties (Dysarthria)': Dysarthria,
                'Vertigo (feeling of spinning)': Vertigo,
                'Tinnitus (ringing in ears)': Tinnitus,
                'Hypoacusis (hearing loss)': Hypoacusis,
                'Diplopia (double vision)': Diplopia,
                'Neurological Defect': Defect,
                'Ataxia (loss of coordination)': Ataxia,
                'Consciousness Altered': Conscience,
                'Paresthesia (abnormal sensation)': Paresthesia,
                'Diabetes Pedigree Function (DPF)': DPF
                }



                    

            pdf_path = create_pdf('Migraine', user_inputs, migraine_diagnosis)

                    # Provide download link for PDF

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(

                label="Download Prediction Report",
                # href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Heart_Failure_Disease_Prediction_Report.pdf">Download Report</a>',
                #     st.markdown(href, unsafe_allow_html=True),

                data=pdf_file,

                file_name="Migraine_Prediction_Report.pdf",

                mime="application/pdf"
                )
                # if migraine_diagnosis and patient_name:
                #     pdf_data = generate_pdf_report(patient_name, patient_no, migraine_diagnosis, input_data, param_names)
                #     b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                #     href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Migraine_Disease_Prediction_Report.pdf">Download Report</a>'
                #     st.markdown(href, unsafe_allow_html=True)
                # elif not patient_name:
                #     st.warning("Please enter the patient name to generate the report.")


                  # Generate PDF report

                    
                # user_inputs = {
                #     'Age': Age,
                #         'Duration of Headache (in months/years)': Duration,
                #         'Frequency of Headache (per month/week)': Frequency,
                #         'Location of Pain': Location,
                #         'Character of Pain': Character,
                #         'Intensity of Pain (scale 1-10)': Intensity,
                #         'Presence of Nausea': Nausea,
                #         'Presence of Vomiting': Vomit,
                #         'Phonophobia (sensitivity to sound)': Phonophobia,
                #         'Photophobia (sensitivity to light)': Photophobia,
                #         'Visual Symptoms (aura, flashes)': Visual,
                #         'Sensory Symptoms (tingling, numbness)': Sensory,
                #         'Speech Difficulties (Dysphasia)': Dysphasia,
                #         'Speech Difficulties (Dysarthria)': Dysarthria,
                #         'Vertigo (feeling of spinning)': Vertigo,
                #         'Tinnitus (ringing in ears)': Tinnitus,
                #         'Hypoacusis (hearing loss)': Hypoacusis,
                #         'Diplopia (double vision)': Diplopia,
                #         'Neurological Defect': Defect,
                #         'Ataxia (loss of coordination)': Ataxia,
                #         'Consciousness Altered': Conscience,
                #         'Paresthesia (abnormal sensation)': Paresthesia,
                #         'Diabetes Pedigree Function (DPF)': DPF
                #     }

                    

                # pdf_path = create_pdf('Diabetes', user_inputs, migraine_diagnosis)

                #     # Provide download link for PDF

                # with open(pdf_path, "rb") as pdf_file:
                #     st.download_button(

                #     label="Download Prediction Report",

                #     data=pdf_file,

                #     file_name="Diabetes_Prediction_Report.pdf",

                #     mime="application/pdf"

                #         )
                    # except ValueError:

                    # st.error("Please ensure all input values are numeric.")

 

        
#Lung_cancer      
        if sub_choice == "Lung Cancer":
            st.markdown("<h3 style='color: black ;'>Lung Cancer Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                Age=st.text_input("Age")
            with col2:
                Smokes=st.text_input("Smoking Frequency")
            with col1:
                AreaQ=st.text_input("Environmental Quality (0-10)")
            with col2:
                Alkhol=st.text_input("Alcohol Consumption")

            
            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age","Smoking frequency","Environmental quality (0-10)","Alcohol consumption"]    
            lc_diagnosis = ''

            if st.button('Lung Cancer Test Result'):

                user_input = [Age,Smokes,AreaQ,Alkhol]

                user_input = [float(x) for x in user_input]

                lc_prediction = lc_model.predict([user_input])

                if lc_prediction[0] == 1:
                    lc_diagnosis = 'The Person Has Lung Cancer'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {lc_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🫁 Lung Cancer Management Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                💊 <b>1. Follow Medical Treatment Strictly</b><br>
                                - Adhere closely to your doctor’s treatment plan, which may include surgery, chemotherapy, radiation, immunotherapy, or targeted therapy.<br>
                                - Attend all appointments and follow up for scans and blood tests.<br><br>
                            
                                🫶 <b>2. Don’t Be Afraid to Ask Questions</b><br>
                                - Understand your diagnosis, treatment options, side effects, and prognosis.<br>
                                - Keep a notebook for symptoms, questions, and advice from your care team.<br><br>
                            
                                🚭 <b>3. Stop Smoking (if applicable)</b><br>
                                - Quitting improves treatment success and helps preserve remaining lung function.<br>
                                - Seek support through cessation programs or medications if needed.<br><br>
                            
                                🍲 <b>4. Focus on Nutrition</b><br>
                                - Eat small, frequent, nutrient-rich meals to combat weight loss or fatigue.<br>
                                - Include fruits, vegetables, whole grains, and lean protein.<br>
                                - Work with a dietitian for cancer-specific nutrition guidance.<br><br>
                            
                                🏃 <b>5. Stay Active When Possible</b><br>
                                - Light activity like walking can improve energy, reduce stress, and support lung function.<br>
                                - Movement also helps prevent blood clots and improves mood.<br><br>
                            
                                😴 <b>6. Prioritize Rest & Recovery</b><br>
                                - Listen to your body and rest when tired.<br>
                                - Nap as needed but try to maintain a basic day-night sleep cycle.<br><br>
                            
                                🧘 <b>7. Manage Stress</b><br>
                                - Try breathing exercises, guided meditation, journaling, or counseling.<br>
                                - Support groups can provide connection and understanding.<br><br>
                            
                                🛡️ <b>8. Protect Your Immune System</b><br>
                                - Avoid crowds during treatment, and maintain good hygiene.<br>
                                - Stay current with recommended vaccines, such as flu or pneumonia shots.<br><br>
                            
                                🫁 <b>9. Use Oxygen Support if Prescribed</b><br>
                                - Oxygen therapy can ease shortness of breath.<br>
                                - Follow instructions on use and storage carefully.<br><br>
                            
                                👨‍⚕️ <b>10. Work Closely with Your Care Team</b><br>
                                - Report any new or worsening symptoms promptly.<br>
                                - Don’t hesitate to talk about pain management, emotional support, or palliative care options.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    lc_diagnosis = 'The Person Has Not Lung Cancer'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {lc_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌿 Suggestions for Maintaining Lung Health (Non-Lung Cancer Individuals)"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                🏃 <b>1. Stay Active</b><br>
                                - Regular exercise helps keep the lungs and cardiovascular system strong.<br>
                                - Activities like walking, swimming, or cycling can improve lung capacity and oxygen efficiency.<br>
                                - Aim for 30 minutes of moderate exercise most days of the week.<br><br>
                            
                                🚭 <b>2. Avoid Smoking</b><br>
                                - Never start smoking, and if you do smoke, seek help to quit.<br>
                                - Secondhand smoke can also affect lung health, so avoid exposure.<br><br>
                            
                                🍎 <b>3. Eat a Healthy Diet</b><br>
                                - A diet rich in fruits, vegetables, whole grains, and lean proteins supports your immune system and overall health.<br>
                                - Antioxidants (like those in berries, spinach, and nuts) protect your lungs from oxidative stress.<br><br>
                            
                                🧴 <b>4. Limit Exposure to Pollutants</b><br>
                                - Stay away from areas with heavy air pollution and hazardous chemicals.<br>
                                - Ensure good air quality at home by using air purifiers and keeping windows open for ventilation.<br><br>
                            
                                🛌 <b>5. Get Quality Sleep</b><br>
                                - Aim for 7–9 hours of sleep every night to allow the body and lungs to rest and rejuvenate.<br>
                                - Good sleep promotes overall health and supports the respiratory system.<br><br>
                            
                                🧼 <b>6. Practice Good Hygiene</b><br>
                                - Wash your hands frequently to reduce the risk of respiratory infections.<br>
                                - Stay away from sick individuals and get vaccinated for flu and pneumonia when recommended.<br><br>
                            
                                🌬️ <b>7. Practice Deep Breathing Exercises</b><br>
                                - Deep breathing exercises (such as diaphragmatic breathing) help strengthen your lungs and improve oxygen intake.<br>
                                - Regular practice of relaxation techniques like yoga can reduce stress and enhance respiratory health.<br><br>
                            
                                🌬️ <b>8. Keep Your Environment Clean</b><br>
                                - Regularly clean dust, mold, and pet dander from your home.<br>
                                - HEPA filters can help reduce allergens and irritants in the air, improving lung health.<br><br>
                            
                                🧘‍♀️ <b>9. Manage Stress Effectively</b><br>
                                - Chronic stress can affect overall health, including your lungs.<br>
                                - Practice relaxation techniques, such as deep breathing, mindfulness, or meditation.<br><br>
                            
                                🩺 <b>10. Regular Health Check-ups</b><br>
                                - Regular check-ups with your doctor help monitor and maintain good health, including lung function.<br>
                                - Ask your doctor about lung screenings if you're at higher risk, such as being a long-term smoker.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if lc_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, lc_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Lung_Cancer_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")

#Kidney_stone
        if sub_choice == "Kidney Stones":
            st.markdown("<h3 style='color: black ;'>Kidney Stones Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: black !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                gravity=st.text_input("Urine Specific Gravity")
            with col1:
                ph=st.text_input("Urine pH")
            with col1:
                osmo=st.text_input("Osmolality")
            with col1:
                cond=st.text_input("Urine Conductivity")
            with col1:
                urea=st.text_input("Urea Concentration")
            with col1:
                calc=st.text_input("Calcium Concentration")

            st.markdown("<h4 style='color: black;'>Patient Information</h4>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Urine Specific Gravity","Urine pH","Osmolality","Urine Conductivity","Urea Concentration","Calcium Concentration"]
 

            # code for Prediction
            ks_diagnosis = ''

            if st.button('Kidney Stones Test Result'):

                user_input = [gravity,ph,osmo,cond,urea,calc]

                # user_input = [float(x) for x in user_input]

                ks_prediction = ks_model.predict(scaler.fit_transform([user_input]))

                if ks_prediction[0] == 1:
                    ks_diagnosis = 'The Person Has Kidney Stone'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {ks_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧑‍⚕️ Suggestions for Kidney Stones Management & Prevention"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                💧 <b>1. Stay Hydrated</b><br>
                                - Drink plenty of water throughout the day to dilute urine substances that lead to stones.<br>
                                - Aim for 2 to 3 liters (8 to 12 cups) daily, adjusted to your climate and needs.<br>
                                - Citrus drinks like lemonade or lime water can help prevent calcium oxalate stones.<br><br>
                            
                                🍏 <b>2. Maintain a Kidney-Friendly Diet</b><br>
                                - Limit foods high in oxalate (spinach, beets, nuts, chocolate) and pair them with calcium-rich foods.<br>
                                - Reduce salt intake to lower calcium in urine.<br>
                                - Ensure adequate dietary calcium (1,000–1,200 mg/day).<br>
                                - Limit animal protein to reduce uric acid stone risk.<br>
                                - Eat more fruits and vegetables to maintain a healthy urine pH.<br><br>
                            
                                🚶‍♀️ <b>3. Stay Active</b><br>
                                - Regular exercise supports a healthy metabolism and helps prevent weight gain.<br>
                                - Maintain a healthy weight to reduce kidney stone risk.<br><br>
                            
                                🧴 <b>4. Limit Sugar and Processed Foods</b><br>
                                - Cut back on sugar, especially fructose in sweetened beverages.<br>
                                - Avoid processed foods high in sodium and unhealthy fats.<br><br>
                            
                                🧂 <b>5. Limit Sodium (Salt) Intake</b><br>
                                - Stick to a low-sodium diet (< 2,300 mg/day).<br>
                                - Avoid salty snacks, canned, or fast foods.<br><br>
                            
                                🩺 <b>6. Monitor Urinary pH</b><br>
                                - Certain stones form in acidic or alkaline urine—monitor pH if advised by your doctor.<br>
                                - Diet and hydration can help balance urine pH.<br><br>
                            
                                🥛 <b>7. Get Enough Calcium, but Don't Overdo It</b><br>
                                - Dietary calcium helps bind oxalates and reduce stone risk.<br>
                                - Avoid excess calcium supplements unless prescribed.<br><br>
                            
                                🧘‍♂️ <b>8. Manage Medical Conditions</b><br>
                                - Control conditions like gout, diabetes, or hyperparathyroidism.<br>
                                - Follow your doctor's plan and take medications as directed.<br><br>
                            
                                💊 <b>9. Medications (if prescribed)</b><br>
                                - Thiazide diuretics: reduce calcium in urine.<br>
                                - Potassium citrate: reduces urine acidity.<br>
                                - Allopurinol: lowers uric acid for uric acid stones.<br><br>
                            
                                🔬 <b>10. Regular Medical Check-ups</b><br>
                                - Urine tests and imaging (ultrasound or CT scans) can help detect or monitor stones.<br>
                                - Follow up as recommended by your healthcare provider.<br><br>
                            
                                🚭 <b>11. Avoid Excessive Caffeine and Alcohol</b><br>
                                - Too much caffeine can increase calcium in urine.<br>
                                - Excessive alcohol causes dehydration and raises stone risk.<br><br>
                            
                                🧴 <b>12. Herbal Remedies (Consult with Your Doctor)</b><br>
                                - Herbs like chanca piedra may help, but always check with your doctor first.<br><br>
                            
                                ⚖️ <b>13. Avoid Dehydration</b><br>
                                - Drink water regularly, especially in hot weather or during physical activity.<br>
                                - Dehydration is a key factor in stone formation.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    ks_diagnosis = 'The Person Have Not Kidney Stones'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {ks_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧑‍⚕️ Suggestions for General Kidney & Urinary Health"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'> 
                            
                                💧 <b>1. Stay Well Hydrated</b><br>
                                - Drink plenty of water daily to support kidney filtration and flush out toxins.<br>
                                - Proper hydration reduces the risk of urinary tract infections (UTIs) and helps regulate blood pressure.<br>
                                - Aim for 8–10 glasses of water per day (more if you're physically active or in a hot climate).<br><br>
                            
                                🍎 <b>2. Eat a Kidney-Friendly Diet</b><br>
                                - Focus on low-sodium, low-fat, and moderate-protein meals.<br>
                                - Eat fruits and vegetables rich in antioxidants (e.g., berries, red bell peppers, cabbage).<br>
                                - Limit foods high in phosphorus and potassium if you have impaired kidney function (e.g., bananas, oranges, dairy, and tomatoes).<br><br>
                            
                                🚭 <b>3. Avoid Smoking and Excessive Alcohol</b><br>
                                - Smoking reduces blood flow to the kidneys and increases the risk of chronic kidney disease (CKD).<br>
                                - Alcohol in excess can dehydrate you and put strain on the kidneys.<br><br>
                            
                                🧂 <b>4. Limit Salt and Processed Foods</b><br>
                                - High sodium intake raises blood pressure and can damage the kidneys.<br>
                                - Avoid packaged or canned foods, instant noodles, salty snacks, and processed meats.<br><br>
                            
                                🧘‍♀️ <b>5. Manage Stress and Get Enough Sleep</b><br>
                                - Chronic stress and poor sleep patterns are linked to hypertension, a leading cause of kidney damage.<br>
                                - Practice relaxation techniques like deep breathing, yoga, or mindfulness.<br><br>
                            
                                🩺 <b>6. Control Blood Pressure and Blood Sugar</b><br>
                                - Uncontrolled high blood pressure and diabetes are the top causes of kidney disease.<br>
                                - Monitor your levels regularly and take medications as prescribed.<br>
                                - Maintain a healthy weight to reduce strain on the kidneys.<br><br>
                            
                                🧪 <b>7. Get Regular Health Screenings</b><br>
                                - Regular urine and blood tests can help detect kidney issues early (e.g., elevated creatinine, proteinuria).<br>
                                - Screen for urinary tract infections if experiencing symptoms like burning urination, frequent urge, or cloudy urine.<br><br>
                            
                                🧴 <b>8. Be Cautious with OTC Medications</b><br>
                                - Avoid overuse of painkillers (e.g., ibuprofen, aspirin, naproxen) which can harm kidney tissue.<br>
                                - Consult your doctor before using herbal supplements, as some may be nephrotoxic.<br><br>
                            
                                🧃 <b>9. Choose Healthy Beverages</b><br>
                                - Choose water, coconut water, or unsweetened herbal teas.<br>
                                - Limit sugary drinks and colas, which may contribute to metabolic issues and increase CKD risk.<br><br>
                            
                                🚶‍♂️ <b>10. Exercise Regularly</b><br>
                                - Aim for 30 minutes of physical activity most days of the week.<br>
                                - Exercise helps maintain blood pressure, blood sugar, and body weight—key factors in kidney health.<br><br>
                            
                                🧼 <b>11. Maintain Good Hygiene</b><br>
                                - Proper hygiene can prevent bladder infections, especially in women.<br>
                                - Wipe front to back and avoid harsh personal hygiene products.<br><br>
                            
                                🚱 <b>12. Avoid Holding Urine Too Long</b><br>
                                - Regularly empty your bladder to avoid bacterial buildup and bladder overdistension, which may impact kidney function.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if ks_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, ks_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Kidney_Stone_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
    
#Heart_failure           
        if sub_choice == "Heart Failure":
            st.subheader("Heart Failure Prediction")
            col1, col2, col3 = st.columns(3)
            with col1:
                age=st.text_input("Age")
            with col2:
                # o=[0,1]
                sex=st.selectbox("Gender",options=[ "Male", "Female"])
                sex = 0 if sex == "Female" else 1
            with col3:
                cp=st.text_input("Chest Pain")
            with col1:
                trestbps=st.text_input("Resting Blood Pressure")
            with col2:
                chol=st.text_input("Cholesterol")
            with col3:
                fbs=st.selectbox("Fasting Blood Sugar" ,options=["Yes" ,"No"])
                fbs = 0 if fbs == "No" else 1
            with col1:
                restecg=st.text_input("Resting Electrocardiographic")
            with col2:
                thalach=st.text_input("Maximum Heart Rate Achieved During Test")
            with col3:
                # ot=[1,0]
                exang=st.selectbox("Exercise-Induced Angina",options=["Yes" ,"No"])
                exang = 0 if exang == "No" else 1
            with col1:
                oldpeak=st.text_input("Oldpeak")
            with col2:
                # op=[0,1,2]
                # slope=st.selectbox("slope(0 = upsloping,1 = flat,2 = downsloping)",op)
                label_to_value = {
                    "Upsloping": 0,
                    "Flat": 1,
                    "Downsloping": 2
                }
                slope = st.selectbox("Slope", list(label_to_value.keys()))
                slope = label_to_value[slope]
            with col3:
                ca=st.text_input("Ca (0-3)")
            with col1:
                label_to_value = {
                    "Normal": 1,
                    "Fixed defect": 2,
                    "Reversible defect": 3
                }
                thal = st.selectbox("Thalassemia", list(label_to_value.keys()))
                thal = label_to_value[thal]
            st.markdown("<h4 style='color: black;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["age","Gender","Chest Pain","Resting blood pressure","Cholesterol","Fasting blood sugar",
                           "Resting electrocardiographic","Maximum heart rate achieved during test","Exercise-induced angina"
                          ,"oldpeak","slope","ca (0-3)","Thalassemia"]
            

            heartF_diagnosis = ''

            if st.button('Heart Failure Test Result'):

                user_input = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]

                user_input = [float(x) for x in user_input]

                heartF_prediction = heartF_model.predict([user_input])

                if heartF_prediction[0] == 1:
                    heartF_diagnosis = 'The Person Has Heart Failure'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {heartF_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: black;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("❤️‍🔥 Heart Failure Patient Care Tips"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                🥦 <b>1. Follow a Low-Sodium Diet</b><br>
                                - Limit sodium to &lt;1500 mg/day.<br>
                                - Avoid canned soups, processed meats (bacon, sausages, deli), packaged/fast foods.<br>
                                - Cook at home using herbs and spices instead of salt.<br>
                                🧂 Less salt = less fluid retention = less strain on your heart.<br><br>
                            
                                💧 <b>2. Manage Fluid Intake (as per doctor’s advice)</b><br>
                                - Some heart failure patients need fluid restriction (1.5–2 liters/day).<br>
                                - Track all fluids: soups, tea, ice, etc.<br>
                                - Weigh yourself daily — sudden weight gain may signal fluid buildup.<br><br>
                            
                                🏃 <b>3. Stay Active — But Smart</b><br>
                                - Light/moderate activity as tolerated (walking, tai chi, seated exercises).<br>
                                - Avoid overexertion — stop if dizzy, breathless, or very tired.<br>
                                - Follow a cardiac rehab plan if recommended.<br><br>
                            
                                💊 <b>4. Take Medications Exactly as Prescribed</b><br>
                                - Don’t skip or double doses.<br>
                                - Common meds: ACE inhibitors, beta-blockers, diuretics.<br>
                                - Keep an updated list of meds; set reminders or use a pill organizer.<br><br>
                            
                                ⚖️ <b>5. Track Daily Weight</b><br>
                                - Weigh each morning after peeing, before eating, in similar clothing.<br>
                                - Alert doctor if weight increases &gt;2–3 lbs in a day or 5 lbs in a week.<br><br>
                            
                                🚭 <b>6. Avoid Alcohol & Smoking</b><br>
                                - Quit smoking — it reduces oxygen supply and worsens heart function.<br>
                                - Avoid alcohol unless cleared by your doctor.<br><br>
                            
                                🛌 <b>7. Get Good Rest & Manage Stress</b><br>
                                - Use extra pillows to sleep semi-upright if needed.<br>
                                - Reduce stress: reading, prayer, meditation, music.<br>
                                - Avoid naps close to bedtime.<br><br>
                            
                                👨‍⚕️ <b>8. Know When to Seek Help</b><br>
                                - Contact your doctor if you notice:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Swelling in legs/feet<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Increased breathlessness<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Chest pain<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Sudden fatigue/weakness<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Irregular heartbeat<br>
                                🩺 Early signs of worsening heart failure can be subtle — don’t wait.<br><br>
                            
                                ✅ <b>Summary for Heart Failure Patients:</b><br>
                                "Eat light, move right, rest well, and check weight daily."<br>
                                Stay closely connected with your care team.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    heartF_diagnosis = 'The Person Does Not Have A Heart Failure'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {heartF_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: black;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("💓 Heart-Healthy Lifestyle Tips (No Heart Failure)"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                🥗 <b>1. Eat a Heart-Friendly Diet</b><br>
                                - Focus on: fruits 🍎, vegetables 🥦, whole grains 🌾, lean proteins (fish 🐟, tofu, beans), and healthy fats (olive oil, nuts).<br>
                                - Limit: red meats, added sugars 🍰, trans & saturated fats, excess sodium.<br>
                                🍽️ Try the DASH or Mediterranean diet for a solid heart base.<br><br>
                            
                                🏃‍♂️ <b>2. Exercise Regularly</b><br>
                                - Aim for 150 mins/week of moderate activity (e.g., brisk walking 🚶‍♀️, swimming 🏊, biking 🚴).<br>
                                - Include 2 days/week of strength training.<br>
                                🫀 Exercise improves heart function, circulation, and blood pressure.<br><br>
                            
                                🚭 <b>3. Don’t Smoke</b><br>
                                - Smoking damages blood vessels and weakens the heart over time.<br>
                                - If you smoke, talk to your doctor about quit plans — it’s never too late to stop.<br><br>
                            
                                ⚖️ <b>4. Maintain a Healthy Weight</b><br>
                                - Extra weight = extra workload for your heart.<br>
                                - Aim for a BMI between 18.5–24.9 (if appropriate).<br>
                                - Focus on long-term lifestyle changes, not crash diets.<br><br>
                            
                                💖 <b>5. Manage Stress & Sleep</b><br>
                                - Chronic stress = higher blood pressure and inflammation.<br>
                                - Try deep breathing, yoga 🧘‍♂️, music 🎶, or nature walks.<br>
                                - Get 7–9 hours of quality sleep each night.<br><br>
                            
                                🩺 <b>6. Stay on Top of Your Health Checkups</b><br>
                                - Regularly monitor: blood pressure, cholesterol levels, and blood sugar (especially if family history of diabetes).<br>
                                - Address any irregularities early.<br><br>
                            
                                🍷 <b>7. Limit Alcohol</b><br>
                                - If you drink, do so in moderation:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Up to 1 drink/day for women<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;- Up to 2 drinks/day for men<br>
                                - Heavy drinking raises blood pressure and heart risk.<br><br>
                            
                                🧬 <b>8. Know Your Family History</b><br>
                                - Some heart problems run in families.<br>
                                - Share your family history with your doctor and stay proactive.<br><br>
                            
                                ✅ <b>Summary:</b><br>
                                "Eat clean, move often, stress less, sleep deep, and check in with your body."<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if  heartF_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no,  heartF_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Heart_Failure_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report. ")                   

            


#COPD
        if sub_choice == "Chronic Obstructive Pulmonary Disease":
            st.subheader("Chronic Obstructive Pulmonary Disease Prediction")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                AGE=st.text_input("AGE")
            with col2:
                PackHistory=st.text_input("Number of pack-years of smoking")
            with col3:
                MWT1Best=st.text_input("Best 6-Minute Walk Tes")
            with col1:
                FEV1=st.text_input("Forced Expiratory Volume in 1 second")
            with col2:
                FEV1PRED=st.text_input("Predicted FEV1")
            with col3:
                FVC=st.text_input("Forced Vital Capacity")
            with col1:
                FVCPRED=st.text_input("Predicted FVC (%)")
            with col2:
                CAT=st.text_input("COPD Assessment Test")
            with col3:
                SGRQ=st.text_input("St.George's Respiratory Questionnaire")
            with col1:
                label_to_value = {
                    "Youngest": 1,
                    "Lower-middle": 2,
                    "Upper-middle": 3,
                    "Oldest": 4
                }
                AGEquartiles = st.selectbox("Categorica of Age", list(label_to_value.keys()))
                AGEquartiles = label_to_value[AGEquartiles]
            with col2:
                gender=st.selectbox("Gender",options=[ "Male", "Female"])
                gender = 0 if gender == "Female" else 1
            with col3:
                Diabetes=st.selectbox("Diabetes",options=[ "Has diabetes", "Does not"])
                Diabetes = 0 if Diabetes == "Does not" else 1
                
            with col1:
                hypertension=st.selectbox("Hypertension",options=[ "Has high blood pressure", "Does not"])
                hypertension = 0 if hypertension == "Does not" else 1
            with col2:
                AtrialFib=st.selectbox("Atrial fibrillation",options=[ "Has atrial fibrillation (irregular heartbeat)", "Does not"])
                AtrialFib = 0 if AtrialFib == "Does not" else 1
            with col3:
                IHD=st.selectbox("Ischemic heart disease",options=[ "Has ischemic heart disease (narrowed heart arteries)", "Does not"])
                IHD = 0 if IHD == "Does not" else 1

            st.markdown("<h4 style='color: black;'>Patient Information</h4>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["AGE","Number of pack-years of smoking","Best 6-Minute Walk Tes","Forced Expiratory Volume in 1 second",
                           "Predicted FEV1","Forced Vital Capacity","Predicted FVC (%)","COPD Assessment Test",
                           "St.George's Respiratory Questionnaire","Categorica of Age","Gender","Diabetes","Hypertension","Atrial fibrillation",
                          "Ischemic heart disease"]
            copd_diagnosis = ''

            if st.button('COPD Test Result'):

                user_input = [AGE,PackHistory,MWT1Best,FEV1,FEV1PRED,FVC,FVCPRED,CAT,SGRQ,AGEquartiles,gender,Diabetes,hypertension,AtrialFib,IHD]

                user_input = [float(x) for x in user_input]

                copd_prediction = copd_model.predict([user_input])
                print(copd_prediction)

                if (copd_prediction == 1):
                    copd_diagnosis = 'The person has first stage of COPD'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: lightgreen;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {copd_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌬️ COPD Stage 1 (Mild) – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: #1C3A3E; font-size: 16px; line-height: 1.6;'>
                            
                                Early-stage COPD may show minimal symptoms. Healthy habits can slow disease progression.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 💨 Use short-acting bronchodilators as prescribed<br>
                                • 🩺 Regular checkups to monitor lung function<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🥦 Eat antioxidant-rich foods (greens, berries)<br>
                                • 💧 Stay hydrated to thin mucus<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🚶 Walk daily to maintain lung and muscle strength<br>
                                • 💨 Practice breathing exercises (pursed-lip breathing)<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 🧘 Light yoga or stretching can ease breathing<br>
                                • 😌 Manage stress through relaxation or hobbies<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🚭 Avoid smoking and secondhand smoke<br>
                                • 🌬️ Ensure clean air at home (use air purifiers if needed)<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                elif (copd_prediction == 2):
                    copd_diagnosis = 'The person has second stage of COPD'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {copd_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌬️ COPD Stage 2 (Moderate) – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: #1C3A3E; font-size: 16px; line-height: 1.6;'>
                            
                                Symptoms become more noticeable; structured management becomes important.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 💊 Use long-acting bronchodilators and inhaled corticosteroids as prescribed<br>
                                • 🫁 Consider pulmonary rehabilitation programs<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🥑 Eat energy-dense, nutritious foods to avoid weight loss<br>
                                • 🚱 Reduce salt to prevent fluid retention<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🏃 Moderate activity within tolerance to improve stamina<br>
                                • 💨 Continue breathing exercises regularly<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 🛁 Warm baths may help relax airways<br>
                                • 🎧 Use guided breathing apps or music therapy<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🧼 Avoid exposure to dust, fumes, and cold air<br>
                                • 📈 Monitor oxygen levels at home if advised by your doctor<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                elif (copd_prediction == 3):
                    copd_diagnosis = 'The person has third stage of COPD'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: lightred;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {copd_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌬️ COPD Stage 3 (Severe) – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: #1C3A3E; font-size: 16px; line-height: 1.6;'>
                            
                                Breathing becomes more difficult; risk of complications increases.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 💉 Use combination inhalers and possibly oxygen therapy<br>
                                • 🏥 More frequent doctor visits and lung function monitoring<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🍽️ Eat smaller, frequent meals to reduce breathlessness<br>
                                • 🧄 Include anti-inflammatory foods (turmeric, garlic)<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🚶 Use mobility aids or rest breaks during walking<br>
                                • 💪 Focus on maintaining muscle mass through light resistance exercises<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 😮‍💨 Breathing retraining with a therapist<br>
                                • 🛏️ Rest and mental relaxation are crucial<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🧯 Create an emergency plan for flare-ups<br>
                                • 🧊 Use humidifiers or warm mist inhalers to ease symptoms<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    copd_diagnosis = 'The person has forth stage of COPD'
                    # st.success(copd_diagnosis)
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {copd_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌬️ COPD Stage 4 (Very Severe) – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: #1C3A3E; font-size: 16px; line-height: 1.6;'>
                            
                                Quality of life is heavily impacted; comprehensive care is vital.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 🩸 Continuous oxygen therapy may be required<br>
                                • 🏥 Regular specialist visits, potential surgical interventions<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🍲 Soft, nutrient-dense foods to ease effort of eating<br>
                                • 🧃 Consider supplements under medical supervision<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🛏️ Rest with light movement as tolerated to prevent deconditioning<br>
                                • 🧍 Use physical therapy for tailored movement plans<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 🧘 Meditation, music, or prayer to support emotional well-being<br>
                                • 🧠 Counseling or support groups for mental health<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🧑‍⚕️ Coordinate palliative care and support<br>
                                • 📞 Keep emergency contacts and equipment ready at home<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if copd_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, copd_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="COPD_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
           
#thyroid
        if sub_choice == "Thyroid Disorders":
            st.markdown("<h3 style='color: white;'>Thyroid Disorders Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3= st.columns(3)
            with col1:
                Age=st.text_input("Age")
            with col2:
                Gender=st.selectbox("Gender",options=["Female", "Male"])
                Gender= 0 if Gender == "Female" else 1
            with col3:
                Smoking=st.selectbox("Smoking",options=["No", "Yes"])
                Smoking = 0 if Smoking == "No" else 1
            with col1:
                Hx_Smoking=st.selectbox("Hx Smoking",options=["No history", "History of smoking"])
                Hx_Smoking = 0 if Hx_Smoking == "No history" else 1
            with col2:
                Hx_Radiothreapy=st.selectbox("Hx Radiothreap",options=["History of radiotherapy", "No history"])
                Hx_Radiothreapy = 0 if Hx_Radiothreapy == "No history" else 1
            with col3:
                Focality=st.selectbox("Focality",options=["Unifocal", "Multifocal tumor"])
                Focality = 0 if Focality == "Unifocal" else 1
            with col1:
                label_to_value = {
                    "low": 0,
                    "intermediate": 1,
                    "high": 2,
                }
                Risk = st.selectbox("Risk", list(label_to_value.keys()))
                Risk = label_to_value[Risk]
            with col2:
                label_to_value = {
                    "No evidence of primary tumor": 0,
                    "Tumor ≤ 2 cm and limited to the thyroid": 1,
                    "Tumor > 2 cm but ≤ 4 cm, still within the thyroid": 2,
                    "Tumor > 4 cm or minimal extrathyroidal extension":3,
                    "Moderate extension beyond the thyroid":4,
                    "More extensive invasion":5,
                    "Tumor cannot be assessed":6
                }
                T = st.selectbox("T", list(label_to_value.keys()))
                T = label_to_value[T]
            with col3:
                label_to_value = {
                    "No regional lymph node metastasis": 0,
                    "Regional lymph node metastasis": 1,
                    "might indicate multiple lymph node groups or large nodes involved": 2,
                }
                N = st.selectbox("N", list(label_to_value.keys()))
                N = label_to_value[N]
            with col1:
                M=st.selectbox("M",options=["No distant metastasis", "Distant metastasis present"])
                M = 0 if M == "No distant metastasis" else 1
            with col2:
                label_to_value = {
                    "Carcinoma in situ (very early)": 0,
                    "Localized, small tumor, no spread": 1,
                    "Larger tumor or local spread": 2,
                    "Regional spread (e.g., lymph nodes)": 3,
                    "Distant spread/metastasis":4
                    
                }
                Stage = st.selectbox("Stage", list(label_to_value.keys()))
                Stage = label_to_value[Stage]
            with col3:
                Thyroid_Function_Clinical_Hypothyroidism=st.selectbox("Thyroid Function Clinical Hypothyroidism",options=["No", "Yes"])
                Thyroid_Function_Clinical_Hypothyroidism = 0 if Thyroid_Function_Clinical_Hypothyroidism == "No" else 1
            with col1:
                Thyroid_Function_Euthyroid=st.selectbox("Thyroid Function Euthyroid",options=["No", "Yes"])
                Thyroid_Function_Euthyroid = 0 if Thyroid_Function_Euthyroid == "No" else 1
            with col2:
                Thyroid_Function_Subclinical_Hyperthyroidism=st.selectbox("Thyroid Function Subclinical Hyperthyroidism",options=["No", "Yes"])
                Thyroid_Function_Subclinical_Hyperthyroidism = 0 if Thyroid_Function_Subclinical_Hyperthyroidism == "No" else 1
            with col3:
                Thyroid_Function_Subclinical_Hypothyroidism=st.selectbox("Thyroid Function Subclinical Hypothyroidism",options=["No", "Yes"])
                Thyroid_Function_Subclinical_Hypothyroidism = 0 if Thyroid_Function_Subclinical_Hypothyroidism == "No" else 1
            with col1:
                Physical_Examination_Multinodular_goiter=st.selectbox("Physical Examination Multinodular goiter",options=["No", "Yes"])
                Physical_Examination_Multinodular_goiter = 0 if Physical_Examination_Multinodular_goiter == "No" else 1
            with col2:
                Physical_Examination_Normal=st.selectbox("Physical_Examination_Normal",options=["No", "Yes"])
                Physical_Examination_Normal = 0 if Physical_Examination_Normal == "No" else 1
            with col3:
                Physical_Examination_Single_nodular_goiter_left=st.selectbox("Physical Examination Single nodular goiter left",options=["No", "Yes"])
                Physical_Examination_Single_nodular_goiter_left = 0 if Physical_Examination_Single_nodular_goiter_left == "No" else 1
            with col1:
                Physical_Examination_Single_nodular_goiter_right=st.selectbox("Physical Examination Single nodular goiter right",options=["No", "Yes"])
                Physical_Examination_Single_nodular_goiter_right = 0 if Physical_Examination_Single_nodular_goiter_right == "No" else 1
            with col2:
                Adenopathy_Extensive=st.selectbox("Adenopathy Extensive",options=["No", "Yes"])
                Adenopathy_Extensive = 0 if Adenopathy_Extensive == "No" else 1
            with col3:
                Adenopathy_Left=st.selectbox("Adenopathy Left",options=["No", "Yes"])
                Adenopathy_Left = 0 if Adenopathy_Left == "No" else 1
            with col1:
                Adenopathy_No=st.selectbox("Adenopathy No",options=["No", "Yes"])
                Adenopathy_No = 0 if Adenopathy_No == "No" else 1
            with col2:
                Adenopathy_Posterior=st.selectbox("Adenopathy Posterior",options=["No", "Yes"])
                Adenopathy_Posterior = 0 if Adenopathy_Posterior == "No" else 1
            with col3:
                Adenopathy_Right=st.selectbox("Adenopathy Right",options=["No", "Yes"])
                Adenopathy_Right = 0 if Adenopathy_Right == "No" else 1
            with col1:
                Pathology_Hurthel_cell=st.selectbox("Pathology Hurthel cell",options=["No", "Yes"])
                Pathology_Hurthel_cell = 0 if Pathology_Hurthel_cell == "No" else 1
            with col2:
                Pathology_Micropapillary=st.selectbox("Pathology Micropapillary",options=["No", "Yes"])
                Pathology_Micropapillary = 0 if Pathology_Micropapillary == "No" else 1
            with col3:
                Pathology_Papillary=st.selectbox("Pathology Papillary",options=["No", "Yes"])
                Pathology_Papillary = 0 if Pathology_Papillary == "No" else 1
            with col1:
                Response_Excellent=st.selectbox("Response Excellent",options=["No", "Yes"])
                Response_Excellent = 0 if Response_Excellent == "No" else 1
            with col2:
                Response_Indeterminate=st.selectbox("Response Indeterminate",options=["No", "Yes"])
                Response_Indeterminate = 0 if Response_Indeterminate == "No" else 1
            with col3:
                Response_Structural_Incomplete=st.selectbox("Response Structural Incomplete",options=["No", "Yes"])
                Response_Structural_Incomplete = 0 if Response_Structural_Incomplete == "No" else 1

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age","Gender","Smoking","Hx Smoking","Hx Radiothreapy","Focality","Risk","T","N","M",
                              "Stage","Thyroid Function Clinical Hypothyroidism",
                              "Thyroid Function Euthyroid",
                              "Thyroid Function Subclinical Hyperthyroidism","Thyroid Function Subclinical Hypothyroidism",
                              "Physical Examination Multinodular goiter","Physical Examination Normal",
                              "Physical Examination Single nodular goiter left","Physical Examination Single nodular goiter right",
                              "Adenopathy Extensive","Adenopathy Left","Adenopathy No","Adenopathy Posterior",
                              "Adenopathy Right","Pathology Hurthel cell","Pathology Micropapillary",
                              "Pathology Papillary","Response Excellent","Response Indeterminate","Response Structural Incomplete"]
            # code for Prediction
            thyroid_diagnosis = ''

            if st.button('Thyroid Disorders Test Result'):

                user_input =[Age,Gender,Smoking,Hx_Smoking,Hx_Radiothreapy,Focality,Risk,T,N,M,
                              Stage,Thyroid_Function_Clinical_Hypothyroidism,
                              Thyroid_Function_Euthyroid,
                              Thyroid_Function_Subclinical_Hyperthyroidism,Thyroid_Function_Subclinical_Hypothyroidism,
                              Physical_Examination_Multinodular_goiter,Physical_Examination_Normal,
                              Physical_Examination_Single_nodular_goiter_left,Physical_Examination_Single_nodular_goiter_right,
                              Adenopathy_Extensive,Adenopathy_Left,Adenopathy_No,Adenopathy_Posterior,
                              Adenopathy_Right,Pathology_Hurthel_cell,Pathology_Micropapillary,
                              Pathology_Papillary,Response_Excellent,Response_Indeterminate,Response_Structural_Incomplete]
                    
                # user_input = [float(x) for x in user_input]

                thyroid_prediction = thyroid_model.predict([user_input])

                if thyroid_prediction[0] == 1:
                    thyroid_diagnosis = 'The Person Have A Thyroid Disorders'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {thyroid_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🦋 Thyroid Disorders – Health & Lifestyle Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions are designed to help individuals manage thyroid disorders and improve overall health.<br><br>
                            
                                🩺 <b>1. Follow Your Treatment Plan</b><br>
                                • Take your thyroid medication (like levothyroxine or anti-thyroid drugs) exactly as prescribed<br>
                                • Take meds on an empty stomach, 30–60 minutes before breakfast for best absorption<br>
                                • Avoid taking with calcium, iron, or soy supplements at the same time<br><br>
                            
                                🍽️ <b>2. Eat a Thyroid-Friendly Diet</b><br>
                                • Include iodine-rich foods (seaweed, iodized salt) – if not overconsuming<br>
                                • Include selenium-rich foods (Brazil nuts, eggs, tuna)<br>
                                • Include zinc-rich foods (pumpkin seeds, legumes)<br>
                                • Avoid excess soy, especially around medication time<br>
                                • Avoid raw goitrogens (like raw cabbage, kale, broccoli) in large amounts — cooking reduces their effects<br>
                                • Overuse of gluten (especially in Hashimoto’s – may help reduce inflammation)<br><br>
                            
                                🧂 <b>3. Watch Iodine Intake Carefully</b><br>
                                • Both deficiency and excess iodine can worsen thyroid function<br>
                                • Use iodized salt in moderation<br><br>
                            
                                🧘 <b>4. Manage Stress</b><br>
                                • Chronic stress affects hormone levels, including TSH<br>
                                • Practice relaxation techniques like deep breathing, journaling, yoga, or meditation<br><br>
                            
                                🧠 <b>5. Track Symptoms & Lab Values</b><br>
                                • Monitor for fatigue, weight changes, mood swings, heart rate, and hair loss<br>
                                • Check TSH, T3, T4, and antibodies regularly with your doctor<br><br>
                            
                                💪 <b>6. Exercise Regularly</b><br>
                                • Regular exercise helps regulate metabolism and mood<br>
                                • For hypothyroidism: start with low-impact exercise like walking, swimming<br>
                                • For hyperthyroidism: avoid high-intensity workouts if experiencing palpitations or tremors<br><br>
                            
                                💤 <b>7. Prioritize Sleep</b><br>
                                • Hormonal imbalances affect sleep quality<br>
                                • Aim for 7–9 hours/night<br>
                                • Keep a consistent bedtime schedule<br><br>
                            
                                ☕ <b>8. Limit Caffeine & Stimulants</b><br>
                                • Especially in hyperthyroidism, caffeine can worsen anxiety and rapid heart rate<br>
                                • Stay hydrated and choose herbal teas<br><br>
                            
                                🧬 <b>9. Family History Awareness</b><br>
                                • Thyroid disorders often run in families<br>
                                • Encourage relatives to get tested if symptoms arise<br><br>
                            
                                💊 <b>10. Avoid Self-Supplementing Without Labs</b><br>
                                • Don’t take iodine, selenium, or glandular thyroid supplements unless tested and prescribed by your doctor<br>
                                • Self-supplementing can worsen thyroid function<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    thyroid_diagnosis = 'The Person Does Not Have A Trhyroid Disorders'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {thyroid_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("✅ Suggestions for People Without Thyroid Disorders"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions focus on preserving thyroid health, maintaining hormonal balance, and promoting general well-being.<br><br>
                            
                                🧂 <b>1. Moderate Iodine Intake</b><br>
                                • Use iodized salt in regular amounts — it’s enough to meet your body’s needs<br>
                                • Avoid excessive iodine supplements or high-iodine diets (e.g., too much seaweed)<br><br>
                            
                                🥦 <b>2. Don’t Overdo Cruciferous Vegetables Raw</b><br>
                                • Broccoli, cabbage, and kale are healthy — but avoid eating them raw in large quantities if iodine-deficient<br>
                                • Light cooking (steaming/sautéing) reduces goitrogenic compounds<br><br>
                            
                                🍽️ <b>3. Eat a Balanced Diet</b><br>
                                • Support thyroid function naturally by including:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Selenium (Brazil nuts, tuna, sunflower seeds)<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Zinc (pumpkin seeds, meat, legumes)<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Iron (spinach, lentils, lean meats)<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Vitamin D & B12 (eggs, salmon, fortified foods)<br>
                                • Limit processed foods and sugar that may cause inflammation<br><br>
                            
                                🧘 <b>4. Manage Stress to Protect Hormonal Balance</b><br>
                                • Chronic stress can disturb the hypothalamic-pituitary-thyroid (HPT) axis<br>
                                • Build daily stress management routines like:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Yoga<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Journaling<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Deep breathing<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Nature walks<br><br>
                            
                                🧠 <b>5. Listen to Your Body for Early Signs</b><br>
                                • Get tested if you experience:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Unusual fatigue<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Sudden weight gain/loss<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Cold sensitivity<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Mood swings or depression<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Irregular menstrual cycles<br><br>
                            
                                💪 <b>6. Stay Physically Active</b><br>
                                • Exercise supports metabolism and hormone balance<br>
                                • Aim for 150 minutes/week of moderate activity (walking, cycling, swimming)<br><br>
                            
                                💤 <b>7. Prioritize Sleep</b><br>
                                • Sleep is essential for hormone repair cycles<br>
                                • Get 7–9 hours/night and keep your circadian rhythm consistent<br><br>
                            
                                🚫 <b>8. Avoid Unnecessary Thyroid Supplements</b><br>
                                • Don’t self-medicate with thyroid boosters, glandular extracts, or high-dose iodine unless prescribed<br>
                                • Overuse can harm your thyroid even if you’re currently healthy<br><br>
                            
                                🧬 <b>9. Know Your Family History</b><br>
                                • Thyroid conditions can be genetic (e.g., Hashimoto’s, Graves’)<br>
                                • If a parent or sibling has thyroid disease, consider screening even if asymptomatic<br><br>
                            
                                🩺 <b>10. Routine Screening (if needed)</b><br>
                                • Yearly thyroid checks aren’t necessary if you're healthy<br>
                                • But if you’re:<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Over 50<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Female (higher risk)<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Have a family history<br>
                                &nbsp;&nbsp;&nbsp;&nbsp;• Or experience symptoms — ask your doctor for a TSH + Free T4 panel<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if thyroid_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, thyroid_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Thyroid_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
            
#sleepDis
        if sub_choice == "Sleep Disorders":
            st.markdown("<h3 style='color: white;'>Sleep Disorders Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                 
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                Age=st.text_input("Age")
            with col2:
                Sleep_Duration=st.text_input("Sleep Duration")
            with col3:
                Quality_of_Sleep=st.text_input("Quality of Sleep (1–10)")
            with col1:
                Stress_Level=st.text_input("Stress Level (1–10)")
            with col2:
                Heart_Rate=st.text_input("Heart Rate")
            with col3:
                Daily_Steps=st.text_input("Daily Steps")
            with col1:
                Systolic_Pressure=st.text_input("Systolic Blood Pressure")
            with col2:
                Diastolic_Pressure=st.text_input("Diastolic Blood Pressure")
            with col3:
                Gender_Male=st.selectbox("Gender",options=["Female", "Male"])
                Gender_Male= 0 if Gender_Male == "Female" else 1
            with col1:
                Occupation_Doctor=st.selectbox("Occupation Doctor",options=["No", "Yes"])
                Occupation_Doctor= 0 if Occupation_Doctor == "No" else 1
            with col2:
                Occupation_Engineer=st.selectbox("Occupation Engineer",options=["No", "Yes"])
                Occupation_Engineer= 0 if Occupation_Engineer == "No" else 1
            with col3:
                Occupation_Lawyer=st.selectbox("Occupation Lawyer",options=["No", "Yes"])
                Occupation_Lawyer= 0 if Occupation_Lawyer == "No" else 1
            with col1:
                Occupation_Manager=st.selectbox("Occupation Manager",options=["No", "Yes"])
                Occupation_Manager= 0 if Occupation_Manager == "No" else 1
            with col2:
                Occupation_Nurse=st.selectbox("Occupation Nurse",options=["No", "Yes"])
                Occupation_Nurse= 0 if Occupation_Nurse == "No" else 1
            with col3:
                Occupation_Salesperson=st.selectbox("Occupation Salesperson",options=["No", "Yes"])
                Occupation_Salesperson= 0 if Occupation_Salesperson == "No" else 1
            with col1:
                Occupation_Scientist=st.selectbox("Occupation Scientist",options=["No", "Yes"])
                Occupation_Scientist= 0 if Occupation_Scientist == "No" else 1
            with col2:
                Occupation_Software_Engineer=st.selectbox("Occupation Software Engineer",options=["No", "Yes"])
                Occupation_Software_Engineer= 0 if Occupation_Software_Engineer == "No" else 1
            with col3:
                Occupation_Teacher=st.selectbox("Occupation Teacher",options=["No", "Yes"])
                Occupation_Teacher= 0 if Occupation_Teacher == "No" else 1
            with col1:
                BMI_Category_Normal_Weight=st.selectbox("BMI Category Normal Weight",options=["No", "Yes"])
                BMI_Category_Normal_Weight= 0 if BMI_Category_Normal_Weight == "No" else 1
            with col2:
                BMI_Category_Overweight=st.selectbox("BMI Category Overweight",options=["No", "Yes"])
                BMI_Category_Overweight= 0 if BMI_Category_Overweight == "No" else 1

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age","Sleep Duration","Quality of Sleep (1–10)","Stress Level (1–10)","Heart Rate","Daily Steps",
                              "Systolic Pressure","Diastolic Pressure","Gender Male","Occupation Doctor",
                              "Occupation Engineer","Occupation Lawyer","Occupation Manager","Occupation Nurse",
                              "Occupation Salesperson","Occupation Scientist","Occupation Software Engineer",
                              "Occupation Teacher","BMI Category Normal Weight","BMI Category Overweight"]
            sleepD_diagnosis = ''

            if st.button('Sleep Disorders Test Result'):

                user_input = [Age,Sleep_Duration,Quality_of_Sleep,Stress_Level,Heart_Rate,Daily_Steps,
                              Systolic_Pressure,Diastolic_Pressure,Gender_Male,Occupation_Doctor,
                              Occupation_Engineer,Occupation_Lawyer,Occupation_Manager,Occupation_Nurse,
                              Occupation_Salesperson,Occupation_Scientist,Occupation_Software_Engineer,
                              Occupation_Teacher,BMI_Category_Normal_Weight,BMI_Category_Overweight]
                # user_input=scaler.fit_transform([user_input])

                # user_input = [float(x) for x in user_input]
                # input_data_as_numpy_array = np.asarray(user_input)
                scaler_input = scaler.fit_transform([user_input])

                sleepD_prediction = sleepD_model.predict(scaler_input)
                # input_data = scaler.fit_transform(user_input)

                # changing the input_data to numpy array
                # input_data_as_numpy_array = np.asarray(input_data)

                # reshape the array as we are predicting for one instance
                # input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

                # prediction = sleepD_model.predict([user_input])
                # print(prediction)

                if sleepD_prediction[0] == 0:
                    sleepD_diagnosis = 'The Person Has Sleep Disorders'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {sleepD_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("💤 Suggestions for Managing Sleep Disorders"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                🛏️ <b>1. Establish a Consistent Sleep Schedule</b><br>
                                - Go to bed and wake up at the same time every day, even on weekends.<br>
                                - Helps regulate your body’s internal clock (circadian rhythm).<br><br>
                            
                                📵 <b>2. Limit Screen Time Before Bed</b><br>
                                - Avoid screens (phone, laptop, TV) at least 1 hour before bedtime.<br>
                                - Blue light suppresses melatonin, the hormone that helps you sleep.<br><br>
                            
                                🌙 <b>3. Create a Relaxing Bedtime Routine</b><br>
                                - Try calming activities: reading, meditation, warm bath, or soft music.<br>
                                - This signals your body that it’s time to wind down.<br><br>
                            
                                🛋️ <b>4. Improve Your Sleep Environment</b><br>
                                - Keep your bedroom cool, dark, and quiet.<br>
                                - Use blackout curtains, white noise machines, or sleep masks if needed.<br>
                                - Invest in a comfortable mattress and pillow.<br><br>
                            
                                ☕ <b>5. Avoid Stimulants Late in the Day</b><br>
                                - Limit caffeine (coffee, tea, chocolate) after 2 PM.<br>
                                - Avoid alcohol and nicotine before bedtime — they disrupt sleep cycles.<br><br>
                            
                                🍽️ <b>6. Watch What You Eat Before Bed</b><br>
                                - Avoid heavy, spicy, or large meals within 2–3 hours of bedtime.<br>
                                - If hungry, opt for a light, sleep-friendly snack (e.g., banana, warm milk, yogurt).<br><br>
                            
                                💪 <b>7. Get Regular Physical Activity</b><br>
                                - Exercise promotes better sleep — just not too close to bedtime.<br>
                                - Morning or early afternoon workouts are ideal.<br><br>
                            
                                🧠 <b>8. Manage Stress and Anxiety</b><br>
                                - Try deep breathing, progressive muscle relaxation, or journaling.<br>
                                - If racing thoughts keep you up, write them down before bed.<br><br>
                            
                                📝 <b>9. Keep a Sleep Diary</b><br>
                                - Track your sleep/wake times, quality of sleep, caffeine intake, and exercise.<br>
                                - Helps identify patterns and possible sleep disruptors.<br><br>
                            
                                👩‍⚕️ <b>10. Consult a Sleep Specialist</b><br>
                                - If symptoms persist (e.g., insomnia, snoring, gasping awake, restless legs), consult a healthcare provider.<br>
                                - Conditions like sleep apnea, narcolepsy, or chronic insomnia need professional care.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                    
                else:
                    sleepD_diagnosis = 'The Person Does Not Have A Sleep Disorders'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {sleepD_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)          
                    with st.expander("🌟 Suggestions for Maintaining Healthy Sleep (Non Sleep Disorder Individuals)"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                ⏰ <b>1. Stick to a Sleep Routine</b><br>
                                - Go to bed and wake up at the same time every day to keep your body clock stable.<br>
                                - Even if you feel you don’t need it now, this prevents future sleep irregularities.<br><br>
                            
                                💡 <b>2. Get Natural Light During the Day</b><br>
                                - Spend some time outdoors or by a window during daylight.<br>
                                - Helps keep your circadian rhythm aligned.<br><br>
                            
                                🧘 <b>3. Practice Wind-Down Activities</b><br>
                                - Before bed, relax your mind and body: light stretching, journaling, meditation, or calming music.<br><br>
                            
                                🛏️ <b>4. Make Your Bedroom Sleep-Friendly</b><br>
                                - Keep it quiet, cool, dark, and reserved for sleep only.<br>
                                - Avoid working or eating in bed to mentally associate it only with sleep.<br><br>
                            
                                🍽️ <b>5. Eat & Drink Smart</b><br>
                                - Avoid heavy meals and caffeine in the evening.<br>
                                - Limit alcohol and sugary snacks before bedtime.<br><br>
                            
                                📱 <b>6. Cut Down on Evening Screen Time</b><br>
                                - Reduce exposure to blue light from phones, tablets, or TVs at least 1 hour before bed.<br><br>
                            
                                🏃 <b>7. Stay Active During the Day</b><br>
                                - Regular physical activity improves sleep quality.<br>
                                - Just try to finish intense exercise at least 2–3 hours before bedtime.<br><br>
                            
                                🚫 <b>8. Avoid Long Daytime Naps</b><br>
                                - Limit naps to 20–30 minutes to avoid interfering with nighttime sleep.<br><br>
                            
                                📊 <b>9. Reflect on Your Sleep Quality</b><br>
                                - Pay attention to how you feel during the day.<br>
                                - If you’re often tired, irritable, or unfocused, your sleep may need improvement — even if you think you’re getting enough.<br><br>
                            
                                👩‍⚕️ <b>10. Stay Proactive About Health</b><br>
                                - Manage underlying conditions (e.g., anxiety, blood sugar, blood pressure) that could impact sleep long-term.<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                     # Generate PDF report
                    # if sleepD_diagnosis and patient_name:
                    #     try:
                    #         pdf_data = generate_pdf_report(patient_name, patient_no, sleepD_diagnosis, user_input, param_names)
                    #         b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    #         href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="SleepDisorder_Disease_Prediction_Report.pdf">Download Report</a>'
                    #         st.markdown(href, unsafe_allow_html=True)
                    #     except Exception as e:
                    #         st.error(f"Error generating PDF: {e}")
                    # elif not patient_name:
                    #     st.warning("Please enter the patient name to generate the report.")


                user_inputs = {
                    'Patient Name':patient_name,
                    'Age': Age,
                    'Sleep Duration (hours)': Sleep_Duration,
                    'Quality of Sleep (1-5)': Quality_of_Sleep,
                    'Stress Level (1-10)': Stress_Level,
                    'Heart Rate (bpm)': Heart_Rate,
                    'Daily Steps': Daily_Steps,
                    'Systolic Pressure (mm Hg)': Systolic_Pressure,
                    'Diastolic Pressure (mm Hg)': Diastolic_Pressure,
                    'Gender: Male (1=Yes, 0=No)': Gender_Male,
                    'Occupation: Doctor': Occupation_Doctor,
                    'Occupation: Engineer': Occupation_Engineer,
                    'Occupation: Lawyer': Occupation_Lawyer,
                    'Occupation: Manager': Occupation_Manager,
                    'Occupation: Nurse': Occupation_Nurse,
                    'Occupation: Salesperson': Occupation_Salesperson,
                    'Occupation: Scientist': Occupation_Scientist,
                    'Occupation: Software Engineer': Occupation_Software_Engineer,
                    'Occupation: Teacher': Occupation_Teacher,
                    'BMI Category: Normal Weight': BMI_Category_Normal_Weight,
                    'BMI Category: Overweight': BMI_Category_Overweight
                }


                    

                pdf_path = create_pdf('Sleep Disorder', user_inputs, sleepD_diagnosis)

                    # Provide download link for PDF

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(

                    label="Download Prediction Report",

                    data=pdf_file,

                    file_name="SleepDisorder_Prediction_Report.pdf",

                    mime="application/pdf"

                        )







                    # if sleepD_diagnosis and patient_name:
                    #     pdf_data = generate_pdf_report(patient_name, patient_no, sleepD_diagnosis, user_input, param_names)
                    #     b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    #     href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="SleepDisorder_Disease_Prediction_Report.pdf">Download Report</a>'
                    #     st.markdown(href, unsafe_allow_html=True)
                    # elif not patient_name:
                    #     st.warning("Please enter the patient name to generate the report.")
            

#obesity
        if sub_choice == "Obesity & Metabolic Syndrome":
            st.markdown("<h3 style='color: white;'>Obesity & Metabolic Syndrome Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                Age=st.text_input("Age")
            with col2:
                Height=st.text_input("Height")
            with col3:
                Weight=st.text_input("Weight")
            with col1:
                FCVC=st.text_input("Frequency of consumption of vegetables")
            with col2:
                NCP=st.text_input("Number of main meals per day")
            with col3:
                CH2O=st.text_input("Daily water consumption")
            with col1:
                FAF=st.text_input("Physical activity frequency")
            with col2:
                TUE=st.text_input("Time using technology devices")
            with col3:
                Gender_Male=st.selectbox("Gender",options=[ "Male", "Female"])
                Gender_Male = 0 if Gender_Male == "Female" else 1
            with col1:
                family_history_yes=st.selectbox("Family history yes",options=["No", "Yes"])
                family_history_yes= 0 if family_history_yes == "No" else 1
            with col2:
                FAVC_yes=st.selectbox("High-calorie food",options=["No", "Yes"])
                FAVC_yes= 0 if FAVC_yes == "No" else 1
            with col3:
                CAEC_Frequently=st.selectbox("Eats food between meals frequently",options=["No", "Yes"])
                CAEC_Frequently= 0 if CAEC_Frequently == "No" else 1
            with col1:
                CAEC_Sometimes=st.selectbox("Eats food between meals sometimes",options=["No", "Yes"])
                CAEC_Sometimes= 0 if CAEC_Sometimes == "No" else 1
            with col2:
                CAEC_no=st.selectbox("Does not eat between meals",options=["No", "Yes"])
                CAEC_no= 0 if CAEC_no == "No" else 1
            with col3:
                SMOKE_yes=st.selectbox("SMOKE",options=["No", "Yes"])
                SMOKE_yes= 0 if SMOKE_yes == "No" else 1
            with col1:
                SCC_yes=st.selectbox("Self-Care Consciousness",options=["No", "Yes"])
                SCC_yes= 0 if SCC_yes == "No" else 1
            with col2:
                CALC_Frequently=st.selectbox("Frequently Consumes Alcohol",options=["No", "Yes"])
                CALC_Frequently= 0 if CALC_Frequently == "No" else 1
            with col3:
                CALC_Sometimes=st.selectbox("Sometimes Consumes Alcohol",options=["No", "Yes"])
                CALC_Sometimes= 0 if CALC_Sometimes == "No" else 1
            with col1:
                CALC_no=st.selectbox("Does Not Consume Alcohol",options=["No", "Yes"])
                CALC_no= 0 if CALC_no == "No" else 1
            with col2:
                MTRANS_Bike=st.selectbox("Uses A Bike",options=["No", "Yes"])
                MTRANS_Bike= 0 if MTRANS_Bike == "No" else 1
            with col3:
                MTRANS_Motorbike=st.selectbox("Uses A Motorbike",options=["No", "Yes"])
                MTRANS_Motorbike= 0 if MTRANS_Motorbike == "No" else 1
            with col1:
                MTRANS_Public_Transportation=st.selectbox("Uses Transportation",options=["No", "Yes"])
                MTRANS_Public_Transportation= 0 if MTRANS_Public_Transportation == "No" else 1
            with col2:
                MTRANS_Walking=st.selectbox("Walks As Main Transport",options=["No", "Yes"])
                MTRANS_Walking= 0 if MTRANS_Walking == "No" else 1

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Age","Height","Weight","Frequency of consumption of vegetables","Number of main meals per day",
                           "Daily water consumption","Physical activity frequency","Time using technology devices","Gender",
                               "Family history yes","High-calorie food","Eats food between meals frequently","Eats food between meals sometimes",
                               "Does not eat between meals","SMOKE","Self-care consciousness","Frequently consumes alcohol",
                           "Sometimes consumes alcohol","Does not consume alcohol","Uses a bike","Uses a Motorbike",
                           "Uses Transportation","Walks as main transport"]
            Obesity_diagnosis = ''

            if st.button('Obesity Test Result'):

                user_input = [Age,Height,Weight,FCVC,NCP,CH2O,FAF,TUE,Gender_Male,
                               family_history_yes,FAVC_yes,CAEC_Frequently,CAEC_Sometimes,
                               CAEC_no,SMOKE_yes,SCC_yes,CALC_Frequently,CALC_Sometimes,
                               CALC_no,MTRANS_Bike,MTRANS_Motorbike,MTRANS_Public_Transportation,MTRANS_Walking]
                # user_input=scaler.fit_transform(user_input)

                # user_input = [float(x) for x in user_input]
                # input_data_as_numpy_array = np.asarray(user_input)
                

                Obesity_prediction = Obesity_model.predict(scaler.fit_transform([user_input]))
                # input_data = scaler.fit_transform(user_input)

                # changing the input_data to numpy array
                # input_data_as_numpy_array = np.asarray(input_data)

                # reshape the array as we are predicting for one instance
                # input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

                prediction = Obesity_model.predict([user_input])
                print(prediction)

                if Obesity_prediction[0] == 1:
                    Obesity_diagnosis = 'The Person Have A Obesity'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {Obesity_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🩺 Obesity & Metabolic Syndrome: Patient Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                <b>Metabolic Syndrome</b> includes a cluster of conditions — increased blood pressure, high blood sugar, excess abdominal fat, and abnormal cholesterol levels — which raise your risk of heart disease, diabetes, and stroke.<br><br>
                            
                                🍽️ <b>1. Adopt a Mediterranean or DASH Diet</b><br>
                                <u>Focus on:</u><br>
                                🥗 Vegetables and fruits (colorful, fiber-rich)<br>
                                🥜 Healthy fats (olive oil, nuts, seeds, avocado)<br>
                                🐟 Lean proteins (fish, poultry, legumes)<br>
                                🍞 Whole grains (brown rice, oats, quinoa)<br>
                                <u>Reduce:</u><br>
                                🍟 Trans fats, saturated fats<br>
                                🍰 Sugary foods & beverages<br>
                                🍞 Refined carbs (white bread, pastries)<br><br>
                            
                                🧘 <b>2. Aim for 5–10% Weight Loss</b><br>
                                - Even a small reduction in weight can improve blood pressure, blood sugar, and cholesterol.<br>
                                - Set realistic goals (e.g., 0.5–1 kg/week)<br><br>
                            
                                🏃 <b>3. Increase Physical Activity</b><br>
                                - At least 150 minutes/week of moderate-intensity exercise:<br>
                                  • Brisk walking<br>
                                  • Swimming<br>
                                  • Cycling<br>
                                - Include 2+ strength training sessions/week to boost metabolism and muscle mass<br><br>
                            
                                🚶 <b>4. Sit Less, Move More</b><br>
                                - Break up long sitting periods every 30–60 minutes<br>
                                - Use a standing desk or walk during calls<br><br>
                            
                                🧂 <b>5. Cut Back on Sodium</b><br>
                                - Reduce salt to <2,300 mg/day (ideally 1,500 mg)<br>
                                - Check food labels: processed and canned foods are common salt sources<br><br>
                            
                                🧃 <b>6. Avoid Sugary Drinks</b><br>
                                - Replace sodas/juices with:<br>
                                  • Water<br>
                                  • Sparkling water<br>
                                  • Herbal tea<br>
                                - Excess sugar drives insulin resistance and belly fat<br><br>
                            
                                🧠 <b>7. Manage Stress</b><br>
                                - Chronic stress increases cortisol → more belly fat & insulin resistance<br>
                                - Try:<br>
                                  • Meditation<br>
                                  • Journaling<br>
                                  • Talking to a therapist<br><br>
                            
                                🛏️ <b>8. Prioritize Sleep (7–9 hrs/night)</b><br>
                                - Poor sleep affects hunger hormones & metabolism<br>
                                - Stick to regular sleep/wake times and reduce screen use at night<br><br>
                            
                                🧪 <b>9. Regular Health Monitoring</b><br>
                                - Track:<br>
                                  • Blood pressure<br>
                                  • Fasting glucose or HbA1c<br>
                                  • Lipid profile (HDL, LDL, triglycerides)<br>
                                  • Waist circumference<br>
                                - Early detection helps prevent complications<br><br>
                            
                                💊 <b>10. Medication & Doctor’s Guidance</b><br>
                                - If lifestyle changes aren’t enough, your doctor may prescribe:<br>
                                  • Metformin for insulin resistance<br>
                                  • Statins for high cholesterol<br>
                                  • Antihypertensives for high BP<br>
                                - Never self-medicate — always follow medical supervision<br><br>
                            
                                🫀 <b>11. Understand the Long-Term Risks</b><br>
                                - If untreated, metabolic syndrome can lead to:<br>
                                  • Type 2 Diabetes<br>
                                  • Heart Disease<br>
                                  • Stroke<br>
                                  • Liver disease (NAFLD)<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    Obesity_diagnosis = 'The Person Have Not Obesity'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {Obesity_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🛡️ Prevention: Non-Obesity & Non-Metabolic Syndrome Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These tips help maintain a healthy metabolic profile, normal body weight, and reduce risks for diabetes, heart disease, stroke, and fatty liver disease.<br><br>
                            
                                🥗 <b>1. Stick to a Balanced Diet (Even Without Symptoms)</b><br>
                                Continue eating:<br>
                                ✅ Whole foods (fruits, vegetables, whole grains, lean proteins)<br>
                                ✅ Healthy fats (nuts, seeds, olive oil)<br>
                                <u>Limit:</u><br>
                                🚫 Processed snacks<br>
                                🚫 Sugary drinks<br>
                                🚫 Excess red/processed meat<br>
                                <u>Why?</u> Metabolic issues often develop silently — eating well keeps systems in check.<br><br>
                            
                                🏃 <b>2. Stay Physically Active</b><br>
                                Maintain at least:<br>
                                • 30 min/day of moderate-intensity movement (brisk walk, bike)<br>
                                • 2x/week strength training (resistance bands, bodyweight, weights)<br>
                                • Keep NEAT (non-exercise activity thermogenesis) high — walk more, take stairs, stretch often<br><br>
                            
                                📏 <b>3. Monitor Waistline & Weight</b><br>
                                Even with a normal BMI, visceral fat (belly fat) increases metabolic risk<br>
                                Track:<br>
                                • Waist circumference (keep < 40 in men, < 35 in women)<br>
                                • Weight trends (not just one number)<br><br>
                            
                                🧂 <b>4. Limit Salt & Hidden Sugars</b><br>
                                Cook at home more often<br>
                                Read labels for:<br>
                                • 🧂 Sodium (< 2,300 mg/day)<br>
                                • 🍬 Added sugars (< 25g/day)<br><br>
                            
                                😴 <b>5. Keep Sleep Clean & Consistent</b><br>
                                Sleep 7–9 hours/night<br>
                                Keep sleep-wake schedule consistent<br>
                                Avoid eating large meals late at night<br><br>
                            
                                🧠 <b>6. Protect Mental & Metabolic Health</b><br>
                                Practice stress relief:<br>
                                • Mindfulness<br>
                                • Nature walks<br>
                                • Hobbies<br>
                                <u>Chronic stress</u> can lead to cortisol elevation → weight gain & insulin resistance<br><br>
                            
                                🔬 <b>7. Do Preventive Health Screenings</b><br>
                                Annual or bi-annual checks for:<br>
                                • Blood pressure<br>
                                • Lipid panel<br>
                                • Fasting blood sugar or HbA1c<br>
                                • Liver function (ALT/AST)<br><br>
                            
                                🍻 <b>8. Limit Alcohol Consumption</b><br>
                                Excess alcohol contributes to belly fat & liver strain<br>
                                Recommended:<br>
                                • ≤ 1 drink/day (women)<br>
                                • ≤ 2 drinks/day (men)<br><br>
                            
                                🚫 <b>9. Avoid "Crash Diets" or "Magic Pills"</b><br>
                                Sudden weight loss can rebound<br>
                                Balanced approach wins in the long run<br><br>
                            
                                ❤️ <b>10. Celebrate & Maintain Good Health</b><br>
                                Keep doing what works — prevention is cheaper and easier than treatment<br>
                                Encourage healthy habits in family/friends too<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)


                if Obesity_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, Obesity_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Obesity_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")

           
#AIDS
        if sub_choice == "HIV/AIDS":
            st.markdown("<h3 style='color: white;'>HIV/AIDS Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                time=st.text_input("Time")
            with col2:
                label_to_value = {
                    "Control group or placebo": 0,
                    "Treatment regimen A": 1,
                    "Treatment regimen B": 2,
                    "Treatment regimen C":3
                }
                trt = st.selectbox("Treatment group", list(label_to_value.keys()))
                trt = label_to_value[trt]
            with col3:
                age=st.text_input("Age")
            with col1:
                wtkg=st.text_input("Weight")
            with col2:
                hemo=st.selectbox("Hemophilia",options=[ "No anemia", "Anemia condition present"])
                hemo = 0 if hemo == "No anemia" else 1
            with col3:
                homo=st.selectbox("Homosexual",options=[ "Homosexual", "Not homosexual"])
                homo = 0 if homo == "Not homosexual" else 1
            with col1:
                drugs=st.selectbox("Intravenous Drug",options=[ "Intravenous drug use history", "Non-IV drug"])
                drugs = 0 if drugs == "Non-IV drug" else 1
            with col2:
                karnof=st.text_input("Karnofsky Performance Score")
            with col3:
                oprior=st.selectbox("Prior Opportunistic",options=[ "Prior OIs present", "No prior opportunistic infections"])
                oprior = 0 if oprior == "No prior opportunistic infections" else 1
            with col1:
                z30=st.selectbox("Prior Use Of Zidovudine",options=[ "Previously treated with zidovudine", "No prior use of zidovudine"])
                z30 = 0 if z30 == "No prior use of zidovudine" else 1
            with col2:
                preanti=st.text_input("Prior Antiretroviral Therapy")
            with col3:
                race=st.selectbox("Race Of Participant",options=[ "Black", "White"])
                race = 0 if race == "White" else 1
            with col1:
                gender=st.selectbox("Gender",options=[ "Male", "Female"])
                gender = 0 if gender == "Female" else 1
            with col2:
                str2=st.selectbox("Stratum 2",options=[ "Participant belongs to one stratum group", "Participant belongs to another group"])
                str2 = 0 if str2 == "Participant belongs to one stratum group" else 1
            with col3:
                label_to_value = {
                    "CD4 < 200": 1,
                    "CD4 between 200–500": 2,
                    "CD4 > 500":3
                }
                strat = st.selectbox("Stratification Variable", list(label_to_value.keys()))
                strat = label_to_value[strat]
            with col1:
                symptom=st.selectbox("Symptom",options=[ "severe", "None"])
                symptom = 0 if symptom == "None" else 1
            with col2:
                treat=st.selectbox("Treatment",options=[ "Received treatment", "No treatment"])
                treat = 0 if treat == "No treatment" else 1
            with col3:
                offtrt=st.selectbox("OffTreatment",options=[ "Went off treatment", "Still on treatment"])
                offtrt = 0 if offtrt == "Still on treatment" else 1
            with col1:
                cd40=st.text_input("cd40")
            with col2:
                cd420=st.text_input("cd420")
            with col3:
                cd80=st.text_input("cd80")
            with col1:
                cd820=st.text_input("cd820")

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Time","Treatment group","Age","Weight","Hemophilia","Homosexual","Intravenous drug","Karnofsky performance score"
                          ,"Prior opportunistic","Prior Use of Zidovudine","Prior antiretroviral therapy","Race of participant","Gender"
                           ,"Stratum 2","Stratification variable","Symptom","Treatment","OffTreatment","cd40","cd420","cd80","cd820"
                          ]
 
            
            aids_diagnosis = ''

            if st.button('HIV/AIDS Test Result'):

                user_input = [time,trt,age,wtkg,hemo,homo,drugs,karnof,oprior,
                              z30,preanti,race,gender,str2,strat,symptom,treat,offtrt,cd40,cd420,cd80,cd820]

                # user_input = [float(x) for x in user_input]

                aids_prediction = aids_model.predict([user_input])

                if aids_prediction[0] == 1:
                    aids_diagnosis = 'The Person Has AIDS'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {aids_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("❤️‍🩹 HIV/AIDS Disease Management Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These health strategies focus on managing HIV effectively, strengthening the immune system, and improving overall well-being.<br><br>
                            
                                💊 <b>1. Start and Adhere to Antiretroviral Therapy (ART)</b><br>
                                Take ART medications as prescribed, every day.<br>
                                ART helps:<br>
                                • Lower viral load to undetectable levels<br>
                                • Prevent progression to AIDS<br>
                                • Reduce risk of transmission<br><br>
                            
                                🩺 <b>2. Regular Medical Checkups</b><br>
                                • Monitor CD4 count and viral load regularly<br>
                                • Screen for opportunistic and co-infections (e.g., TB, hepatitis)<br>
                                • Report any side effects or new symptoms promptly<br><br>
                            
                                🛡️ <b>3. Prevent Opportunistic Infections</b><br>
                                • Take prophylactic meds as prescribed (e.g., for PCP, MAC)<br>
                                • Stay up-to-date on vaccines (flu, hepatitis A/B, pneumococcal)<br>
                                • Practice safe food handling to avoid contamination<br><br>
                            
                                🧠 <b>4. Mental Health Support</b><br>
                                • Acknowledge the emotional toll — it's okay to seek help<br>
                                • Join support groups or access professional counseling<br>
                                • Manage stress through mindfulness, journaling, or creative outlets<br><br>
                            
                                🥦 <b>5. Follow a Nutritious Diet</b><br>
                                • Eat balanced meals with lean proteins, veggies, whole grains, and healthy fats<br>
                                • Avoid undercooked meats and unpasteurized dairy<br>
                                • Stay hydrated for kidney and liver health<br><br>
                            
                                🚭 <b>6. Avoid Risky Behaviors</b><br>
                                • Use condoms consistently<br>
                                • Never share needles or sharp items<br>
                                • Limit or quit smoking, alcohol, and recreational drugs<br><br>
                            
                                🏋️ <b>7. Exercise Regularly</b><br>
                                • Aim for 30 minutes of moderate activity most days<br>
                                • Benefits include stronger immunity, better mood, and weight control<br><br>
                            
                                🏡 <b>8. Maintain a Clean Living Environment</b><br>
                                • Reduce exposure to dust, mold, and allergens<br>
                                • Avoid close contact with people who are sick (flu, chickenpox, etc.)<br><br>
                            
                                🧾 <b>9. Disclose with Care</b><br>
                                • Always inform your healthcare providers<br>
                                • Disclose to partners only in safe, trusted situations<br><br>
                            
                                🔄 <b>10. Stay Informed and Empowered</b><br>
                                • Keep up with new research, treatments, and self-care strategies<br>
                                • Follow trusted sources like WHO, CDC, or local HIV networks<br>
                                • Advocate for your health—you are your strongest ally<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)



                else:
                    aids_diagnosis = 'The Person Have Not AIDS'
                    # st.success(aids_diagnosis)
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {aids_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🛡️ HIV/AIDS Prevention & General Immune Health Tips"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These tips are aimed at helping individuals prevent HIV infection and strengthen their immune system naturally.<br><br>
                            
                                🧬 <b>1. Practice Safe Sex</b><br>
                                • Use condoms correctly and consistently<br>
                                • Reduce number of sexual partners or practice mutual monogamy<br>
                                • Get tested regularly for HIV and STIs<br><br>
                            
                                💉 <b>2. Get Tested Periodically</b><br>
                                • Everyone aged 13–64 should be tested at least once<br>
                                • High-risk individuals (e.g., MSM, IV drug users) should test more frequently<br>
                                • Know your partner’s HIV status<br><br>
                            
                                💊 <b>3. Consider Pre-exposure Prophylaxis (PrEP)</b><br>
                                • If you're at high risk, ask your doctor about PrEP<br>
                                • When taken daily, PrEP reduces HIV risk by over 90%<br><br>
                            
                                🩸 <b>4. Avoid Sharing Needles or Sharp Objects</b><br>
                                • Never share syringes, razors, toothbrushes<br>
                                • Only use sterilized equipment for piercings or tattoos<br><br>
                            
                                🧼 <b>5. Maintain Good Hygiene</b><br>
                                • Wash hands regularly, especially before meals<br>
                                • Cover wounds and avoid exposure to body fluids<br><br>
                            
                                🥗 <b>6. Boost Your Immune System Naturally</b><br>
                                • Eat a balanced diet: fruits, veggies, lean proteins, healthy fats<br>
                                • Focus on immune-boosting nutrients: vitamins A, C, D, E, and zinc<br>
                                • Stay well-hydrated<br><br>
                            
                                🏃 <b>7. Exercise Regularly</b><br>
                                • Aim for 150 minutes of moderate activity per week<br>
                                • Benefits include reduced inflammation and stronger immunity<br><br>
                            
                                💤 <b>8. Prioritize Sleep</b><br>
                                • Get 7–9 hours of restful sleep each night<br>
                                • Sleep deprivation weakens immune defense<br><br>
                            
                                🧠 <b>9. Manage Stress</b><br>
                                • Chronic stress suppresses immunity<br>
                                • Use mindfulness, deep breathing, or therapy to cope<br><br>
                            
                                🚭 <b>10. Avoid Risky Habits</b><br>
                                • Don’t smoke or use illicit drugs<br>
                                • Limit alcohol—it can impair immune function<br><br>
                            
                                💬 <b>11. Stay Educated and Aware</b><br>
                                • Learn how HIV is and isn’t transmitted<br>
                                • Participate in public health events and testing drives<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if aids_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, aids_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="AIDS_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
            
#covid
        if sub_choice == "Covid-19":
            st.markdown("<h3 style='color: white;'>Covid-19 Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox> label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput> label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                Breathing_Problem=st.selectbox("Breathing Problem",options=["No", "Yes"])
                Breathing_Problem = 0 if Breathing_Problem == "No" else 1
            with col2:
                Fever=st.selectbox("Fever",options=["No", "Yes"])
                Fever = 0 if Fever == "No" else 1
            with col3:
                Dry_Cough=st.selectbox("Dry Cough",options=["No", "Yes"])
                Dry_Cough = 0 if Dry_Cough == "No" else 1
            with col1:
                Sore_throat=st.selectbox("Sore Throat",options=["No", "Yes"])
                Sore_throat = 0 if Sore_throat == "No" else 1
            with col2:
                Running_Nose=st.selectbox("Running Nose",options=["No", "Yes"])
                Running_Nose = 0 if Running_Nose == "No" else 1
            with col3:
                Asthma=st.selectbox("Asthma",options=["No", "Yes"])
                Asthma = 0 if Asthma == "No" else 1
            with col1:
                Chronic_Lung_Disease=st.selectbox("Chronic Lung Disease",options=["No", "Yes"])
                Chronic_Lung_Disease = 0 if Chronic_Lung_Disease == "No" else 1
            with col2:
                Headache=st.selectbox("Headache",options=["No", "Yes"])
                Headache = 0 if Headache == "No" else 1
            with col3:
                Heart_Disease=st.selectbox("Heart Disease",options=["No", "Yes"])
                Heart_Disease = 0 if Heart_Disease == "No" else 1
            with col1:
                Diabetes=st.selectbox("Diabetes",options=["No", "Yes"])
                Diabetes = 0 if Diabetes == "No" else 1
            with col2:
                Hyper_Tension=st.selectbox("Hyper Tension",options=["No", "Yes"])
                Hyper_Tension = 0 if Hyper_Tension == "No" else 1
            with col3:
                Fatigue=st.selectbox("Fatigue",options=["No", "Yes"])
                Fatigue= 0 if Fatigue == "No" else 1
            with col1:
                Gastrointestinal=st.selectbox("Gastrointestinal",options=["No", "Yes"])
                Gastrointestinal = 0 if Gastrointestinal == "No" else 1
            with col2:
                Abroad_travel=st.selectbox("Abroad Travel",options=["No", "Yes"])
                Abroad_travel = 0 if Abroad_travel == "No" else 1
            with col3:
                Contact_with_COVID_Patient=st.selectbox("Contact With COVID Patient",options=["No", "Yes"])
                Contact_with_COVID_Patient = 0 if Contact_with_COVID_Patient == "No" else 1
            with col1:
                Attended_Large_Gathering=st.selectbox("Attended Large Gathering",options=["No", "Yes"])
                Attended_Large_Gathering = 0 if Attended_Large_Gathering == "No" else 1
            with col2:
                Visited_Public_Exposed_Places=st.selectbox("Visited Public Exposed Places",options=["No", "Yes"])
                Visited_Public_Exposed_Places = 0 if Visited_Public_Exposed_Places == "No" else 1
            with col3:
                Family_working_in_Public_Exposed_Places=st.selectbox("Family Working In Public Exposed Places",options=["No", "Yes"])
                Family_working_in_Public_Exposed_Places = 0 if Family_working_in_Public_Exposed_Places == "No" else 1

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Breathing Problem","Fever","Dry Cough","Sore throat","Running Nose","Asthma",
                              "Chronic Lung Disease","Headache","Heart Disease","Diabetes","Hyper Tension","Fatigue",
                              "Gastrointestinal" ,"Abroad travel","Contact with COVID Patient","Attended Large Gathering",
                              "Visited Public Exposed Places","Family working in Public Exposed Places"]           
            covid_diagnosis = ''

            if st.button('Covid-19 Test Result'):

                user_input = [Breathing_Problem,Fever,Dry_Cough,Sore_throat,Running_Nose,Asthma,
                              Chronic_Lung_Disease,Headache,Heart_Disease,Diabetes,Hyper_Tension,Fatigue,
                              Gastrointestinal ,Abroad_travel,Contact_with_COVID_Patient,Attended_Large_Gathering,
                              Visited_Public_Exposed_Places,Family_working_in_Public_Exposed_Places]

                # user_input = [float(x) for x in user_input]

                covid_prediction = covid_model.predict([user_input])

                if covid_prediction[0] == 1:
                    covid_diagnosis = 'The Person Has COVID-19'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {covid_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🦠 COVID-19 Disease Management & Recovery Tips"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                Practical, up-to-date suggestions for individuals diagnosed with COVID-19, focusing on mild to moderate cases managed at home.<br><br>
                            
                                🏠 <b>1. Isolate & Prevent Spread</b><br>
                                • Stay in a well-ventilated room away from others, including pets<br>
                                • Use a separate bathroom if available<br>
                                • Wear a mask around others and encourage household members to do the same<br><br>
                            
                                💧 <b>2. Stay Hydrated</b><br>
                                • Drink plenty of fluids (water, warm soups, ORS if needed)<br>
                                • Dehydration can worsen fatigue, fever, and dizziness<br><br>
                            
                                🌡️ <b>3. Monitor Symptoms Regularly</b><br>
                                • Check temperature and oxygen levels 2–3 times daily<br>
                                • Watch for warning signs: SpO₂ &lt; 94%, chest pain, confusion, bluish lips/face, or difficulty breathing<br><br>
                            
                                🤒 <b>4. Manage Symptoms Supportively</b><br>
                                • Use paracetamol or acetaminophen for fever, body aches<br>
                                • Steam inhalation or saline sprays for congestion<br>
                                • Cough syrups or lozenges for sore throat<br><br>
                            
                                🍲 <b>5. Eat Immune-Supportive Foods</b><br>
                                • Include vitamin C-rich fruits & veggies, protein (dal, eggs, tofu, lean meats)<br>
                                • Add ginger, turmeric, garlic for anti-inflammatory support<br>
                                • Avoid processed, greasy, or sugary foods<br><br>
                            
                                🛌 <b>6. Get Plenty of Rest</b><br>
                                • Sleep 7–9 hours daily and avoid physical exertion<br>
                                • Even with mild symptoms, rest supports immune recovery<br><br>
                            
                                💊 <b>7. Take Prescribed Medications</b><br>
                                • Follow doctor's advice for antivirals (e.g., Paxlovid), steroids (if needed)<br>
                                • Take supplements like Vitamin D, Zinc, B-complex as advised<br><br>
                            
                                💬 <b>8. Stay in Touch With Healthcare Providers</b><br>
                                • Use telemedicine for regular check-ins<br>
                                • Report worsening symptoms or side effects promptly<br><br>
                            
                                📆 <b>9. Follow Isolation Protocol</b><br>
                                • Isolate 5–10 days based on local health authority guidelines<br>
                                • End isolation after 24 hrs fever-free (without meds), improved symptoms, and full duration<br><br>
                            
                                🧠 <b>10. Care for Your Mental Health</b><br>
                                • Try deep breathing, meditation, or talk with loved ones online<br>
                                • Avoid excessive news or anxiety-inducing media<br><br>
                            
                                🛡️ <b>11. Support Long-Term Health</b><br>
                                • Watch for “long COVID” symptoms: fatigue, brain fog, discomfort<br>
                                • Resume exercise slowly and mindfully<br><br>
                            
                                💉 <b>12. Stay Updated on Vaccination</b><br>
                                • Stay current on booster shots, especially if immunocompromised or 60+<br>
                                • Vaccination reduces severity and future risk<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    covid_diagnosis = 'The Person Have Not COVID-19'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {covid_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧍‍♂️ Non-COVID Health Maintenance Suggestions"):
                            st.markdown("""
                            <div style='color: white; font-size: 16px; line-height: 1.6;'>
                        
                            These tips focus on maintaining good health and wellness for individuals without COVID-19, with an emphasis on prevention, boosting immunity, and overall well-being.<br><br>
                        
                            💉 <b>1. Stay Up to Date on Vaccinations</b><br>
                            • Keep your COVID-19 vaccines and boosters current<br>
                            • Get your annual flu shot and other recommended vaccines (e.g., pneumonia, tetanus, shingles)<br><br>
                        
                            🧼 <b>2. Practice Good Hygiene</b><br>
                            • Wash hands frequently with soap and water for 20+ seconds<br>
                            • Use hand sanitizer when soap isn’t available<br>
                            • Avoid touching your face with unwashed hands<br><br>
                        
                            🧘 <b>3. Support Immune Health</b><br>
                            • Eat a balanced diet with fruits, vegetables, whole grains, and lean protein<br>
                            • Stay hydrated—aim for 2–3 liters of water per day<br>
                            • Get at least 7–8 hours of sleep each night<br>
                            • Practice stress management (meditation, yoga, breathing exercises)<br><br>
                        
                            🏃 <b>4. Stay Physically Active</b><br>
                            • Aim for at least 30 minutes of moderate activity (like walking, dancing, cycling) 5 days/week<br>
                            • Include strength and flexibility exercises like stretching or yoga<br><br>
                        
                            🏠 <b>5. Ensure Proper Ventilation</b><br>
                            • Keep indoor spaces well-ventilated, especially when people are gathered<br>
                            • Open windows or use air purifiers to keep air fresh<br><br>
                        
                            🧑‍⚕️ <b>6. Attend Regular Health Checkups</b><br>
                            • Schedule routine health screenings:<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Blood pressure, blood sugar, cholesterol<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Eye and dental exams<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Cancer screenings (as per age group)<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Follow up on chronic conditions like diabetes, asthma, or hypertension<br><br>
                        
                            😷 <b>7. Avoid Crowded or Poorly Ventilated Spaces When Sick</b><br>
                            • Even if it's not COVID-19, other illnesses like flu, RSV, or common cold can spread easily<br>
                            • Stay home when you’re sick and avoid close contact with others<br><br>
                        
                            🧠 <b>8. Care for Mental Well-being</b><br>
                            • Stay connected with friends and family<br>
                            • Limit screen time and take digital breaks<br>
                            • Seek help if experiencing anxiety, depression, or burnout<br><br>
                        
                            📱 <b>9. Keep a Personal Health Record</b><br>
                            • Use an app or notebook to track:<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Vitals, medications, allergies<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Symptoms or changes in your health<br>
                            &nbsp;&nbsp;&nbsp;&nbsp;• Lab reports or medical appointments<br><br>
                        
                            🌿 <b>10. Avoid Harmful Habits</b><br>
                            • Limit or quit smoking and alcohol consumption<br>
                            • Avoid self-medicating or using antibiotics unnecessarily<br>
                            • Reduce processed foods and excess sugar/salt intake<br><br>
                        
                            </div>
                            """, unsafe_allow_html=True)

                if covid_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, covid_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Covid19_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
        
#Asthma
        if sub_choice == "Asthma":
            st.markdown("<h3 style='color: black;'>Asthma Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: black !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: black !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                DustExposure=st.text_input("DustExposure (0-10)")
            with col2:
                GastroesophagealReflux=st.selectbox("Binary indicator of acid reflux" ,options=["No", "Yes"])
                GastroesophagealReflux = 0 if GastroesophagealReflux == "No" else 1
            with col1:
                LungFunctionFEV1=st.text_input("LungFunctionFEV1")
            with col2:
                LungFunctionFVC=st.text_input("LungFunctionFVC")
            with col1:
                Wheezing=st.selectbox("Presence Of Wheezing Sounds",options=["No", "Yes"])
                Wheezing = 0 if Wheezing == "No" else 1    
            with col2:
                ChestTightness=st.selectbox("Tightness In The Chest",options=["No", "Yes"])
                ChestTightness = 0 if ChestTightness == "No" else 1
            with col1:
                Coughing=st.selectbox("frequency Of Coughing",options=["No", "Yes"])
                Coughing = 0 if Coughing == "No" else 1
            with col2:
                NighttimeSymptoms=st.selectbox("Symptoms Like Coughing Or Wheezing During The Night", options=["No", "Yes"])
                NighttimeSymptoms = 0 if NighttimeSymptoms == "No" else 1
            with col1:
                ExerciseInduced=st.selectbox("Symptoms Triggered By Exercise", options=["No", "Yes"])
                ExerciseInduced = 0 if ExerciseInduced == "No" else 1

            st.markdown("<h4 style='color: black;'>Patient Information</h4>", unsafe_allow_html=True)
 
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["DustExposure (0-10)","Binary indicator of acid reflux","LungFunctionFEV1","LungFunctionFVC",
                           "Presence of wheezing sounds","Tightness in the chest","frequency of coughing",
                           "Symptoms like coughing or wheezing during the night","Symptoms triggered by exercise"]
            # code for Prediction
            asthma_diagnosis = ''

            if st.button('Asthma Test Result'):

                user_input = [DustExposure,GastroesophagealReflux,LungFunctionFEV1,
                              LungFunctionFVC,Wheezing,ChestTightness,Coughing,NighttimeSymptoms,ExerciseInduced]

                # user_input = [float(x) for x in user_input]

                asthma_prediction = asthma_model.predict([user_input])

                if asthma_prediction[0] == 1:
                    asthma_diagnosis = 'The person Has Asthma'
                    st.success(asthma_diagnosis)
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {asthma_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌬️ Asthma Disease Management Suggestions"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                These practical suggestions aim to help individuals with asthma manage their symptoms and improve their quality of life.<br><br>
                            
                                💊 <b>1. Follow Your Asthma Action Plan</b><br>
                                • Work with your doctor to create a personalized Asthma Action Plan<br>
                                • Take medications as prescribed — including inhalers, corticosteroids, or bronchodilators<br><br>
                            
                                📆 <b>2. Monitor Your Symptoms</b><br>
                                • Keep a daily symptom journal or use a peak flow meter to track lung function<br>
                                • Share trends with your healthcare provider for timely adjustments<br><br>
                            
                                🧹 <b>3. Avoid Common Triggers</b><br>
                                • Allergens: Dust mites, pollen, mold, pet dander<br>
                                • Irritants: Smoke, pollution, strong odors, cleaning sprays<br>
                                • Keep your home clean, well-ventilated, and fragrance-free when possible<br><br>
                            
                                🏠 <b>4. Use Air Filters</b><br>
                                • Consider using a HEPA filter in your bedroom and replace HVAC filters regularly<br><br>
                            
                                🤧 <b>5. Manage Allergies</b><br>
                                • If allergies worsen asthma, talk to your doctor about antihistamines or allergy shots (immunotherapy)<br><br>
                            
                                🚫 <b>6. Avoid Smoking (and Secondhand Smoke)</b><br>
                                • Smoking is one of the worst asthma triggers<br>
                                • Avoid smoke-filled areas and ask friends/family to respect smoke-free zones<br><br>
                            
                                🧘 <b>7. Practice Breathing Techniques</b><br>
                                • Techniques like pursed-lip breathing or Buteyko breathing may help during attacks<br>
                                • Consider yoga or mindfulness to improve breathing control<br><br>
                            
                                🏃‍♂️ <b>8. Exercise Wisely</b><br>
                                • Regular exercise helps improve lung function — warm up first and use a reliever inhaler if prescribed<br>
                                • Avoid outdoor exercise in cold air or high pollution<br><br>
                            
                                🤒 <b>9. Prevent Respiratory Infections</b><br>
                                • Get the flu vaccine annually and stay up to date with COVID-19 boosters<br>
                                • Wash hands often and avoid sick people when possible<br><br>
                            
                                🩺 <b>10. Regular Check-Ups</b><br>
                                • Visit your doctor even if you feel well — asthma can silently worsen<br>
                                • Review your medications and triggers regularly<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    asthma_diagnosis = 'The Person Have Not Asthmar'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {asthma_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🌿 Wellness Suggestions for Non-Asthmatic Individuals"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions aim to help individuals maintain good respiratory health and overall well-being.<br><br>
                            
                                🧘‍♀️ <b>1. Maintain Healthy Lungs</b><br>
                                • Practice deep breathing exercises to strengthen lung capacity<br>
                                • Avoid exposure to dust, pollution, smoke, and harsh chemicals<br><br>
                            
                                🚭 <b>2. Avoid Smoking</b><br>
                                • Don't start smoking, and avoid secondhand smoke<br>
                                • Even occasional exposure to smoke can irritate the lungs over time<br><br>
                            
                                🧼 <b>3. Keep Indoor Air Clean</b><br>
                                • Use air purifiers or maintain proper ventilation<br>
                                • Avoid excessive use of scented candles, incense, or aerosol sprays<br><br>
                            
                                🏃‍♂️ <b>4. Exercise Regularly</b><br>
                                • Aerobic exercises like walking, swimming, or cycling improve lung function and circulation<br>
                                • Exercise also boosts your immune system<br><br>
                            
                                🥦 <b>5. Eat a Balanced Diet</b><br>
                                • A diet rich in fruits, vegetables, whole grains, and lean protein supports lung and overall health<br>
                                • Antioxidants (like those in berries, spinach, and nuts) help protect lung tissue<br><br>
                            
                                🛌 <b>6. Prioritize Sleep</b><br>
                                • Aim for 7–9 hours of quality sleep per night<br>
                                • Good sleep supports the immune system and lung repair processes<br><br>
                            
                                💧 <b>7. Stay Hydrated</b><br>
                                • Drinking enough water helps keep mucous membranes moist and improves breathing comfort<br><br>
                            
                                💉 <b>8. Keep Up With Vaccinations</b><br>
                                • Stay current with flu shots, COVID-19 vaccines, and pneumonia prevention if at risk<br><br>
                            
                                🧴 <b>9. Prevent Respiratory Infections</b><br>
                                • Wash your hands frequently<br>
                                • Avoid close contact with people who are sick<br>
                                • Consider wearing a mask in crowded or dusty environments<br><br>
                            
                                🧠 <b>10. Stay Informed and Preventive</b><br>
                                • Regular check-ups with your healthcare provider can help detect any early signs of lung issues or other conditions<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if asthma_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, asthma_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Asthma_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")                    

            

#Chronic Kidney disease
        if sub_choice == "Chronic Kidney Disease":
            st.markdown("<h3 style='color: white;'>Chronic Kidney Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stSelectbox > label {
                      color: white !important;  / Set label color to black /
                      }
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3 = st.columns(3)
            # with col1:
            #     id=st.text_input("id")
            with col1:
                age=st.text_input("Age")
            with col2:
                bp=st.text_input("Blood Pressure")
            with col3:
                sg=st.text_input("Specific Gravity Of Urine")
            with col1:
                al=st.text_input("Albumin In urine (0–5 Scale)")
            with col2:
                su=st.text_input("Sugar In Urine (0–5 Scale)")
            with col3:
                rbc = st.selectbox("Red Blood Cells In Urine", options=["Normal", "Abnormal"])
                rbc = 0 if rbc == "Normal" else 1
            with col1:
                pc = st.selectbox("Pus Cells In Urine", options=["Normal", "Abnormal"])
                pc = 0 if pc == "Normal" else 1
            with col2:
                pcc = st.selectbox("Pus Cell Clumps", options=["Not present", "Present"])
                pcc = 0 if pcc == "Not present" else 1
            with col3:
                ba = st.selectbox("Bacteria", options=["Not present", "Present"])
                ba = 0 if ba == "Not present" else 1
            with col1:
                bgr=st.text_input("Blood Glucose Random")
            with col2:
                bu=st.text_input("Blood Urea")
            with col3:
                sc=st.text_input("Serum Creatinine")
            with col1:
                sod=st.text_input("Sodium")
            with col2:
                pot=st.text_input("Potassium")
            with col3:
                hemo=st.text_input("Hemoglobin")
            with col1:
                pcv=st.text_input("Packed Cell Volume")
            with col2:
                wc=st.text_input("White Blood Cell Count")
            with col3:
                rc=st.text_input("Red Blood Cell Count")
            with col1:
                htn = st.selectbox("Hypertension:", options=["No", "Yes"])
                htn = 0 if htn == "No" else 1
            with col2:
                dm = st.selectbox("Diabetes Mellitus:", options=["No", "Yes"])
                dm = 0 if dm == "No" else 1
            with col3:
                # cad=st.text_input("Coronary Artery Disease 0 = No,1 = Yes")
                cad = st.selectbox("Coronary Artery Disease", options=["No", "Yes"])
                cad = 0 if cad == "No" else 1
            with col1:
                appet = st.selectbox("Appetite", options=["Good", "Poor"])
                appet = 0 if appet == "Good" else 1            
            with col2:
                pe = st.selectbox("Pedal Edema (Swelling in legs)", options=["No", "Yes"])
                pe = 0 if pe == "No" else 1
            with col3:
                ane = st.selectbox("Anemia", options=["No", "Yes"])
                ane = 0 if ane == "No" else 1

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["age", "Blood pressure", "Specific gravity of urine",
                           "Albumin in urine (0–5 scale)", 
                           "Sugar in urine (0–5 scale)", "Red blood cells in urine", "Pus cells in urine", 
                           "Pus cell clumps", "Bacteria", "Blood glucose random", "Blood urea", "Serum creatinine", 
                           "Sodium", "Potassium", "Hemoglobin", "Packed cell volume", "White blood cell count", 
                           "Red blood cell count", "Hypertension", "Diabetes Mellitus", 
                           "Coronary Artery Disease", "Appetite", "Pedal edema (swelling in legs)", "Anemia"]
            cKidney_diagnosis = ''

            if st.button('Chronic Kidney - Test Result'):

                user_input = [age,bp,sg,al,su,rbc,pc,pcc,ba,bgr,bu,sc,sod,pot,hemo,pcv,wc,rc,htn,dm,cad,appet,pe,ane]

                user_input = [float(x) for x in user_input]

                cKidney_prediction = cKidney_model.predict([user_input])

                if cKidney_prediction[0] == 1:
                    cKidney_diagnosis = 'The Person Has Chronic Kidney'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {cKidney_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🩺 Wellness Suggestions for Chronic Kidney Disease (CKD) Management"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions aim to help individuals with CKD maintain kidney function, slow disease progression, and improve quality of life.<br><br>
                            
                                🩺 <b>1. Adhere to Your Treatment Plan</b><br>
                                • Take medications as prescribed, especially for blood pressure, blood sugar, and cholesterol<br>
                                • Manage underlying conditions like diabetes, hypertension, and heart disease<br><br>
                            
                                🥗 <b>2. Follow a Kidney-Friendly Diet</b><br>
                                • Limit sodium to help manage blood pressure and fluid retention<br>
                                • Control protein intake to avoid overworking the kidneys<br>
                                • Monitor potassium and phosphorus levels based on kidney function<br>
                                • Stay hydrated, but follow fluid intake guidelines<br><br>
                            
                                🏃 <b>3. Stay Active</b><br>
                                • Engage in moderate exercise like walking or swimming (150 minutes per week)<br>
                                • Consult your doctor before starting a new routine<br><br>
                            
                                💧 <b>4. Monitor Blood Pressure</b><br>
                                • Aim for blood pressure under 130/80 mmHg (or as advised)<br>
                                • Take prescribed medications to protect kidney function<br><br>
                            
                                🧴 <b>5. Monitor Blood Sugar (if diabetic)</b><br>
                                • Maintain HbA1c levels in your target range<br>
                                • Follow your diabetes care plan closely<br><br>
                            
                                🩹 <b>6. Avoid Over-the-Counter Medications</b><br>
                                • Limit NSAIDs like ibuprofen, which can damage kidneys<br>
                                • Avoid unapproved supplements and always consult your doctor<br><br>
                            
                                ⚖️ <b>7. Maintain a Healthy Weight</b><br>
                                • A healthy weight supports kidney health and controls comorbid conditions<br><br>
                            
                                🧑‍⚕️ <b>8. Get Regular Kidney Function Tests</b><br>
                                • Track creatinine, GFR, and urine protein to monitor progression<br>
                                • Adjust treatment as needed based on test results<br><br>
                            
                                🚭 <b>9. Quit Smoking</b><br>
                                • Smoking worsens kidney damage and raises risk for heart disease<br>
                                • Seek help if needed to quit<br><br>
                            
                                👨‍⚕️ <b>10. Consult a Nephrologist</b><br>
                                • Regular visits with a kidney specialist ensure personalized care<br>
                                • Early intervention can slow progression<br><br>
                            
                                🛏️ <b>11. Get Enough Rest</b><br>
                                • Aim for 7–9 hours of quality sleep to support overall health<br><br>
                            
                                🍎 <b>12. Manage Stress</b><br>
                                • Practice stress-relief techniques like meditation and deep breathing<br><br>
                            
                                💉 <b>13. Consider Dialysis (if needed)</b><br>
                                • If kidney function declines significantly, dialysis may be necessary<br>
                                • Discuss options like dialysis or transplant early with your doctor<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                    
                else:
                    cKidney_diagnosis = 'The Person Has Not Chronic Kidney'
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {cKidney_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🧑‍⚕️ Wellness Suggestions for Maintaining Healthy Kidneys (Non-CKD)"):
                                st.markdown("""
                                <div style='color: black; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions aim to support individuals who do not have CKD in maintaining overall kidney health and preventing future issues.<br><br>
                            
                                🏃 <b>1. Stay Physically Active</b><br>
                                • Regular activity helps with weight management, blood pressure control, and circulation<br>
                                • Aim for 150 minutes/week of moderate activity like walking, cycling, or swimming<br><br>
                            
                                🍏 <b>2. Follow a Kidney-Healthy Diet</b><br>
                                • Eat fruits, vegetables, whole grains, and lean proteins<br>
                                • Limit processed foods, excess salt, and sugary drinks<br><br>
                            
                                💧 <b>3. Stay Hydrated</b><br>
                                • Water helps kidneys flush out toxins<br>
                                • Aim for 6–8 cups of water daily (adjust for activity level and climate)<br><br>
                            
                                🚭 <b>4. Avoid Smoking</b><br>
                                • Smoking reduces kidney blood flow and increases cardiovascular risk<br>
                                • Seek support to quit if needed<br><br>
                            
                                🩺 <b>5. Monitor Your Blood Pressure</b><br>
                                • Keep blood pressure below 130/80 mmHg<br>
                                • High BP is a leading cause of kidney damage<br><br>
                            
                                🩻 <b>6. Get Regular Health Check-Ups</b><br>
                                • Track kidney function via creatinine and urine albumin tests<br>
                                • Monitor blood sugar and cholesterol as well<br><br>
                            
                                🧘‍♀️ <b>7. Manage Your Weight</b><br>
                                • Maintain a healthy weight to lower risk of diabetes and high BP<br>
                                • Combine diet and regular exercise for best results<br><br>
                            
                                🍔 <b>8. Limit Alcohol Consumption</b><br>
                                • Excessive alcohol affects BP and liver health<br>
                                • Limit to 1 drink/day (women) or 2 drinks/day (men)<br><br>
                            
                                🩺 <b>9. Avoid Overuse of OTC Painkillers</b><br>
                                • NSAIDs like ibuprofen can strain the kidneys<br>
                                • Always follow dosing instructions and avoid chronic use<br><br>
                            
                                🧂 <b>10. Avoid Excessive Salt</b><br>
                                • Too much salt raises blood pressure<br>
                                • Choose fresh foods and season with herbs/spices<br><br>
                            
                                🧴 <b>11. Monitor Your Blood Sugar (if applicable)</b><br>
                                • Uncontrolled diabetes is a major risk for kidney disease<br>
                                • Follow your care plan and maintain healthy lifestyle habits<br><br>
                            
                                👨‍⚕️ <b>12. Get Enough Sleep</b><br>
                                • Aim for 7–9 hours of sleep per night<br>
                                • Sleep supports blood pressure, glucose regulation, and recovery<br><br>
                            
                                🌬️ <b>13. Be Mindful of Environmental Toxins</b><br>
                                • Avoid exposure to smoke, industrial chemicals, and pollutants<br>
                                • Use air purifiers and ventilate indoor spaces<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)


                user_inputs = {
                    'Patient Name':patient_name,
                    'Age': age,
                    'Blood Pressure': bp,
                    'Specific Gravity': sg,
                    'Albumin': al,
                    'Sugar': su,
                    'Red Blood Cells': rbc,
                    'Pus Cell': pc,
                    'Pus Cell Clumps': pcc,
                    'Bacteria': ba,
                    'Blood Glucose Random': bgr,
                    'Blood Urea': bu,
                    'Serum Creatinine': sc,
                    'Sodium': sod,
                    'Potassium': pot,
                    'Hemoglobin': hemo,
                    'Packed Cell Volume': pcv,
                    'White Blood Cell Count': wc,
                    'Red Blood Cell Count': rc,
                    'Hypertension': htn,
                    'Diabetes Mellitus': dm,
                    'Coronary Artery Disease': cad,
                    'Appetite': appet,
                    'Pedal Edema': pe,
                    'Anemia': ane
                }



                    

                pdf_path = create_pdf('Chronic Kidney Disease', user_inputs, cKidney_diagnosis)

                    # Provide download link for PDF

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(

                    label="Download Prediction Report",

                    data=pdf_file,

                    file_name="Chronic_Kidney_Disease_Prediction_Report.pdf",

                    mime="application/pdf"

                        )
                # if cKidney_diagnosis and patient_name:
                #     pdf_data = generate_pdf_report(patient_name, patient_no, cKidney_diagnosis, user_input, param_names)
                #     b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                #     href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Heart_Disease_Prediction_Report.pdf">Download Report</a>'
                #     st.markdown(href, unsafe_allow_html=True)
                # elif not patient_name:
                #     st.warning("Please enter the patient name to generate the report.")

#parkinsons            
        if sub_choice == "Parkinson's Disease":
            st.markdown("<h3 style='color: white;'>Parkinson's Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                fo = st.text_input('MDVP:Fo(Hz)') #Average vocal fundamental frequency (in Hertz) – pitch of the voice
            with col2:
                fhi = st.text_input('MDVP:Fhi(Hz)') #Maximum vocal fundamental frequency
            with col3:
                flo = st.text_input('MDVP:Flo(Hz)') #Minimum vocal fundamental frequency.
            with col4:
                Jitter_percent = st.text_input('MDVP:Jitter(%)') #Percentage variation in fundamental frequency.
            with col5:
                Jitter_Abs = st.text_input('MDVP:Jitter(Abs)') #Absolute jitter (in seconds).
            with col1:
                RAP = st.text_input('MDVP:RAP') #Relative Average Perturbation – short-term jitter.
            with col2:
                PPQ = st.text_input('MDVP:PPQ') #Five-point Period Perturbation Quotient
            with col3:
                DDP = st.text_input('Jitter:DDP') #Derivative of the RAP – higher values suggest more instability.
            with col4:
                Shimmer = st.text_input('MDVP:Shimmer') #Variation in amplitude
            with col5:
                Shimmer_dB = st.text_input('MDVP:Shimmer(dB)') #Shimmer in decibels.
            with col1:
                APQ3 = st.text_input('Shimmer:APQ3') #3-point Amplitude Perturbation Quotient.
            with col2:
                APQ5 = st.text_input('Shimmer:APQ5') #5-point Amplitude Perturbation Quotient.
            with col3:
                APQ = st.text_input('MDVP:APQ') #Another form of shimmer APQ.
            with col4:
                DDA = st.text_input('Shimmer:DDA') #Derivative of APQ – higher values indicate rougher voice.
            with col5:
                NHR = st.text_input('Noise-to-Harmonics Ratio') #Noise-to-Harmonics Ratio – higher in Parkinson's patients
            with col1:
                HNR = st.text_input('Harmonics-to-Noise Ratio') #Harmonics-to-Noise Ratio – higher is generally better (clearer voice).
            with col2:
                RPDE = st.text_input('Recurrence Period Density Entropy') #Recurrence Period Density Entropy – quantifies chaotic structure.
            with col3:
                DFA = st.text_input('Detrended Fluctuation Analysis') #Detrended Fluctuation Analysis – correlates with voice signal complexity.
            with col4:
                spread1 = st.text_input('spread1') #Nonlinear measure of signal – related to frequency distribution.
            with col5:
                spread2 = st.text_input('spread2') #Nonlinear measure – second spread statistic.
            with col1:
                D2 = st.text_input('D2') #Correlation dimension – complexity of signal dynamics.
            with col2:
                PPE = st.text_input('Pitch Period Entropy') #Pitch Period Entropy – how irregular the pitch periods are.

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)",
                           "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)",
                           "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "Noise-to-Harmonics Ratio",
                           "Harmonics-to-Noise Ratio", "Recurrence Period Density Entropy", "Detrended Fluctuation Analysis",
                           "spread1", "spread2", "D2", "Pitch Period Entropy"]
    # code for Prediction
            parkinsons_diagnosis = ''

    # creating a button for Prediction    
            if st.button("Parkinson's Test Result"):
                user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

                user_input = [float(x) for x in user_input]

                parkinsons_prediction = parkinsons_model.predict([user_input])

                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "The Person Has Parkinson's Disease"
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {parkinsons_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("💡 Suggestions for Parkinson's Disease Management"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions are aimed at supporting individuals with Parkinson's Disease in managing symptoms and improving quality of life.<br><br>
                            
                                🧠 <b>1. Medication Management</b><br>
                                • Take prescribed medications (e.g., Levodopa or Dopamine agonists) on a strict schedule to control motor symptoms<br>
                                • Work closely with your healthcare provider to adjust doses as needed<br><br>
                            
                                🤸 <b>2. Regular Exercise</b><br>
                                • Engage in physical activities like walking, swimming, yoga, or tai chi<br>
                                • Exercise improves balance, flexibility, and strength<br><br>
                            
                                🥗 <b>3. Healthy Diet</b><br>
                                • Eat a balanced diet rich in fiber and antioxidants<br>
                                • Consider smaller, frequent meals to avoid fatigue and aid digestion<br><br>
                            
                                🧘 <b>4. Stress Reduction</b><br>
                                • Practice relaxation techniques such as deep breathing, mindfulness, or meditation<br>
                                • These methods help reduce tremors and anxiety<br><br>
                            
                                🗣️ <b>5. Speech Therapy</b><br>
                                • If speech is affected, work with a speech-language pathologist (SLP) to maintain clarity and strength<br><br>
                            
                                🧩 <b>6. Occupational Therapy</b><br>
                                • An OT can recommend tools and modifications for easier and safer daily tasks<br><br>
                            
                                💬 <b>7. Stay Socially Active</b><br>
                                • Stay connected with friends, family, or support groups to combat isolation and depression<br><br>
                            
                                👨‍⚕️ <b>8. Regular Doctor Visits</b><br>
                                • Consistent check-ups with a neurologist ensure monitoring of disease progression and treatment adjustments<br><br>
                            
                                🚫 <b>9. Avoid Triggers</b><br>
                                • Limit alcohol and caffeine intake<br>
                                • Be cautious with medications that may interact poorly with Parkinson's drugs<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    parkinsons_diagnosis = "The Person Does Not Have Parkinson's Disease"
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {parkinsons_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("✅ Suggestions for a Healthy Nervous System"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                These suggestions are aimed at supporting overall brain health and preventing future neurological issues.<br><br>
                            
                                🧠 <b>1. Stay Mentally Active</b><br>
                                • Keep your brain sharp with puzzles, reading, learning new skills, or playing musical instruments<br><br>
                            
                                🏃‍♂️ <b>2. Regular Physical Activity</b><br>
                                • Engage in moderate aerobic exercises like walking, cycling, or swimming<br>
                                • Physical activity helps maintain motor function and overall brain health<br><br>
                            
                                🍎 <b>3. Balanced Diet</b><br>
                                • Eat plenty of leafy greens, berries, omega-3-rich fish, nuts, and whole grains<br>
                                • These foods support neurological function and cognitive health<br><br>
                            
                                😴 <b>4. Prioritize Sleep</b><br>
                                • Aim for 7–9 hours of quality sleep per night<br>
                                • Sleep is essential for brain repair, memory consolidation, and overall well-being<br><br>
                            
                                🧘‍♀️ <b>5. Manage Stress</b><br>
                                • Chronic stress can negatively affect your nervous system<br>
                                • Use yoga, meditation, or deep breathing exercises to manage stress effectively<br><br>
                            
                                🚭 <b>6. Avoid Neurotoxins</b><br>
                                • Avoid smoking, limit alcohol, and steer clear of prolonged exposure to industrial chemicals or pesticides<br><br>
                            
                                🩺 <b>7. Regular Checkups</b><br>
                                • Routine health screenings can help detect early signs of neurological or metabolic conditions<br><br>
                            
                                📵 <b>8. Limit Screen Time</b><br>
                                • Take breaks from screens to reduce eye strain and mental fatigue<br><br>
                            
                                🚶 <b>9. Stay Socially Engaged</b><br>
                                • Meaningful social interactions improve brain resilience, mood, and cognitive function<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)
                if parkinsons_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, parkinsons_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Parkinsons_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")

#Dengue            

        if sub_choice == "Dengue":
            st.markdown("<h3 style='color: white;'>Dengue Disease Prediction</h3>", unsafe_allow_html=True)
            st.markdown(
                 """
                 <style>
                      .stTextInput > label {
                      color: white !important;  / Set label color to black /
                      }
                </style>
                """,
                unsafe_allow_html=True
            )
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                tempmax=st.text_input("Maximum Temperature")
            with col2:
                tempmin=st.text_input("Minimum Temperature")
            with col3:
                temp=st.text_input("Average Temperature")
            with col4:
                feelslikemax=st.text_input("Max Perceived Temperature")
            with col1:
                feelslikemin=st.text_input("Min Terceived Temperature")
            with col2:
                feelslike=st.text_input("Feelslike")
            with col3:
                dew=st.text_input("Dew Point (°C)")
            with col4:
                humidity=st.text_input("Relative Humidity (%)")
            with col1:
                precip=st.text_input("Precipitation Amount")
            with col2:
                precipprob=st.text_input("Probability Of Precipitation")
            with col3:
                precipcover=st.text_input("Precipcover")
            with col4:
                snow=st.text_input("Snow")
            with col1:
                snowdepth=st.text_input("Snowdepth")
            with col2:
                windspeed=st.text_input("Windspeed")
            with col3:
                winddir=st.text_input("Winddir")
            with col4:
                sealevelpressure=st.text_input("Sealevelpressure")
            with col1:
                cloudcover=st.text_input("Cloudcover")
            with col2:
                visibility=st.text_input("Visibility")
            with col3:
                solarradiation=st.text_input("Solarradiation")
            with col4:
                solarenergy=st.text_input("Solarenergy")
            with col1:
                uvindex=st.text_input("Uvindex")
            with col2:
                conditions=st.text_input("Conditions")
            with col3:
                stations=st.text_input("Stations")
            with col4:
                cases=st.text_input("Cases")

            st.markdown("<h4 style='color: white;'>Patient Information</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                patient_name = st.text_input("Patient Name")
            with col1:
                patient_no = st.text_input("Patient Phone Number(Optional)")
                        # Parameter names for Heart Diseases PDF
            param_names = ["Maximum temperature", "Minimum temperature", "Average temperature", "Max perceived temperature",
                           "Min perceived temperature", "feelslike", "Dew point (°C)", "Relative humidity (%)",
                           "Precipitation amount", "Probability of precipitation", "precipcover", "snow",
                           "snowdepth", "windspeed", "winddir", "sealevelpressure", "cloudcover", "visibility",
                           "solarradiation", "solarenergy", "uvindex", "conditions", "stations", "cases"]
            # code for Prediction
            Dengue_diagnosis = ''

            if st.button("Dengue Test Result"):
                user_input = [tempmax,tempmin,temp,feelslikemax,feelslikemin,feelslike,dew,
                              humidity,precip,precipprob,precipcover,snow,snowdepth,windspeed,
                              winddir,sealevelpressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,conditions,stations,cases]

                user_input = [float(x) for x in user_input]

                Dengue_prediction = Dengue_model.predict([user_input])

                if Dengue_prediction[0] == 1:
                    Dengue_diagnosis = "The Person Has Dengue"
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: red;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {Dengue_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🦟 Dengue Fever – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                Dengue is a mosquito-borne viral illness that can range from mild to severe. Timely medical care, rest, and hydration are key to recovery.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 💉 Seek immediate medical care if dengue is suspected, especially with warning signs (abdominal pain, bleeding, fatigue)<br>
                                • ❌ Avoid NSAIDs (like ibuprofen or aspirin) – use paracetamol (acetaminophen) for fever and pain<br>
                                • 🩸 Monitor platelet count and hydration levels regularly under a doctor’s supervision<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🍲 Eat easily digestible, nutritious foods like soup, rice, fruits<br>
                                • 🍊 Include vitamin C-rich foods (oranges, guava) to support immunity<br>
                                • 💧 Stay extremely well-hydrated with water, coconut water, ORS, and fresh juices<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🛌 Complete rest is essential during infection and recovery<br>
                                • 🚫 Avoid any physical activity or strain until fully recovered and cleared by a doctor<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 🧘 Gentle breathing or guided rest can help cope with anxiety during recovery<br>
                                • 🛏️ Prioritize sleep and quiet time to aid healing<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🧊 Cold compresses to reduce fever naturally<br>
                                • 🦟 Use mosquito nets and repellents to prevent bites, especially during the first week of illness (to avoid spreading the virus)<br>
                                • 📆 Monitor for severe symptoms (bleeding, vomiting, confusion) and seek urgent care if they appear<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                else:
                    Dengue_diagnosis = "The Person Does Not Have Dengue"
                    st.markdown(
                        f"""
                        <div style='
                        background-color: #b0e0e6;
                        color: green;
                        padding: 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                        border: 1px solid #f5c6cb;
                        '>
                        {Dengue_diagnosis}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            # Inject custom CSS to style the expander label
                    st.markdown("""
                        <style>
                        [data-testid="stExpander"] > details > summary {
                        background-color: #c0c0c0;
                            color: white;
                        }
                        </style>
                            """, unsafe_allow_html=True)
                    with st.expander("🤒 Non-Dengue Febrile Illness – Wellness Suggestions"):
                                st.markdown("""
                                <div style='color: white; font-size: 16px; line-height: 1.6;'>
                            
                                General febrile illnesses not caused by dengue still require careful management through rest, hydration, and symptom monitoring.<br><br>
                            
                                🩺 <b>Medication & Medical Care</b><br>
                                • 💊 Use paracetamol (acetaminophen) to manage fever and discomfort<br>
                                • 🧑‍⚕️ Consult a doctor if fever lasts more than 3 days or is accompanied by rash, confusion, or breathing issues<br>
                                • 🧪 May require lab tests to rule out other infections (like malaria, typhoid, COVID-19)<br><br>
                            
                                🥗 <b>Diet & Nutrition</b><br>
                                • 🍚 Eat light, bland meals like rice porridge, toast, or soup<br>
                                • 🍎 Include immune-supportive foods like fruits, veggies, and herbal teas<br>
                                • 💧 Drink plenty of fluids – water, ORS, coconut water, and clear broth<br><br>
                            
                                🏃 <b>Exercise & Physical Activity</b><br>
                                • 🛌 Rest is critical to allow the body to fight infection<br>
                                • ❌ Avoid exertion even if fever subsides; allow time to regain strength<br><br>
                            
                                🧘 <b>Therapies & Stress Relief</b><br>
                                • 😌 Deep breathing or light meditation to relax and promote recovery<br>
                                • 📺 Engage in calm activities like reading or music for mental rest<br><br>
                            
                                🌿 <b>Lifestyle & Home Remedies</b><br>
                                • 🧊 Use cold compresses or sponge baths to reduce high fever<br>
                                • 🧴 Apply menthol-based rubs for body aches or nasal congestion<br>
                                • 🧼 Maintain good hygiene to prevent spreading infection to others<br><br>
                            
                                </div>
                                """, unsafe_allow_html=True)

                if Dengue_diagnosis and patient_name:
                    pdf_data = generate_pdf_report(patient_name, patient_no, Dengue_diagnosis, user_input, param_names)
                    b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
                    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Dengue_Disease_Prediction_Report.pdf">Download Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
                elif not patient_name:
                    st.warning("Please enter the patient name to generate the report.")
            


def main():
    load_users()

    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    st.set_page_config(page_title="Health Analyzer UI", layout="wide")
    # Set page config
    logo_path = "Images/Black White Minimalist Professional Initial Logo (5).png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            data = f.read()
            encoded_img = f"data:image/png;base64,{base64.b64encode(data).decode()}"
            st.sidebar.markdown(
                f"""
                <div style="display: flex; justify-content: center;">
                    <img src="{encoded_img}" width="200">
                </div>
                """,
                unsafe_allow_html=True
            )

     # ✅ Add Logo with Reduced Size
    # logo_path = "Images/logo.jpeg"
    # logo_path = "Images/Black White Minimalist Professional Initial Logo (5).png"

    # if os.path.exists(logo_path):
    #     st.sidebar.image(logo_path, width=150,)  # Reduced size

    
    st.sidebar.title("Health Analyzer UI")

    if st.session_state.authenticated:
        page = st.sidebar.radio("Go to", ["Home", "About US","Prediction"])
        if page == "Home": home_page()
        elif page == "About US" : about_us()
        elif page == "Prediction": prediction_page()
        st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("🚪 Logout"): logout()
    else:
        page = st.sidebar.radio("Select a page", ["Login", "Register"])
        if page == "Login": login()
        elif page == "Register": register()

if __name__ == "__main__":
    main()
