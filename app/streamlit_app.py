import streamlit as st
import requests

st.set_page_config(page_title="Churn Predictor", layout="wide")
st.title("Telecom Customer Churn Predictor")
st.write("Fill in the customer details below to see their churn risk.")

# Create a clean form for the user to fill out
with st.form("customer_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure Months", min_value=0, max_value=100, value=12)
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        
    with col2:
        lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        
    with col3:
        tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly = st.number_input("Monthly Charges", min_value=0.0, value=50.0)
        total = st.number_input("Total Charges", min_value=0.0, value=500.0)
        
    submit = st.form_submit_button("Predict Churn Risk")

# What happens when the user clicks the button:
if submit:
    # 1. Package the data exactly how our API (schemas.py) expects it
    customer_data = {
        "Gender": gender, "Senior Citizen": senior, "Partner": partner, 
        "Dependents": dependents, "Tenure Months": tenure, "Phone Service": phone,
        "Multiple Lines": lines, "Internet Service": internet, "Online Security": security,
        "Online Backup": backup, "Device Protection": protection, "Tech Support": support,
        "Streaming TV": tv, "Streaming Movies": movies, "Contract": contract,
        "Paperless Billing": paperless, "Payment Method": payment,
        "Monthly Charges": monthly, "Total Charges": total
    }
    
    # 2. Send it to our API (We will update this link when we put the API on the internet!)
    API_URL = "http://127.0.0.1:8000/predict"
    
    try:
        response = requests.post(API_URL, json=customer_data)
        if response.status_code == 200:
            result = response.json()
            
            # 3. Show the results with a visual progress bar
            st.subheader(f"Risk Band: {result['risk_band']}")
            st.progress(result['churn_probability'])
            st.write(f"**Probability of leaving:** {result['churn_probability'] * 100:.1f}%")
        else:
            st.error("The API rejected the data. Check your inputs.")
    except:
        st.warning("Could not connect to the API yet. This is normal until we deploy it to the internet in the next step!")
