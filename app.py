import streamlit as st
import numpy as np
import joblib

# ---- Page config ----
st.set_page_config(page_title="Churn Prediction", layout="wide")

# ---- CSS ----
st.markdown("""
<style>
/* Main background */
.stApp { background-color: #0E1117; }

/* Main Title */
h1 { color: #FFFFFF !important; font-weight: 900 !important; font-size: 42px !important; text-align: center; }
h1:after { content: ""; display: block; width: 120px; height: 4px; margin: 10px auto 0 auto; background-color: #E50914; border-radius: 10px; }

/* Subheadings */
h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; }

/* Labels */
label { color: #FFFFFF !important; font-weight: 600 !important; }

/* Input text */
input, textarea { color: white !important; }

/* Number inputs (Monthly & Total Charges) */
div[data-baseweb="numberinput"] input {
    color: black !important;
    font-weight: 700 !important;
    background-color: white !important;
}

/* Buttons */
.stButton>button { background-color: #E50914; color: white; border-radius: 10px; font-weight: 600; padding: 0.6em 1.2em; }
.stButton>button:hover { background-color: #b20710; box-shadow: 0 0 10px #E50914; }

/* Divider */
hr { border-color: #444444; }/* Number input text (Monthly & Total Charges) */
div.stNumberInput input {
    color: black !important;          /* text color inside box */
    font-weight: 700 !important;      /* bold text */
    background-color: white !important; /* white box background */
}/* Card container */
.card {
    background-color: #1a1a1a;  /* dark gray card */
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(255, 0, 20, 0.5); /* subtle red shadow */
    margin-bottom: 20px;
}

/* Red glow for number inputs on focus */
div.stNumberInput input:focus {
    outline: 2px solid #E50914 !important;
    box-shadow: 0 0 10px #E50914 !important;
}
</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.title("📊 Customer Churn Prediction System")
st.markdown("Predict whether a telecom customer is likely to churn.")
st.divider()

# ---- Load model + scaler ----
model = joblib.load("xgb_churn_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---- Layout ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Customer Info")
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Has Partner", ["No", "Yes"])
    dependents = st.selectbox("Has Dependents", ["No", "Yes"])
    tenure = st.slider("Tenure (Months)", 0, 72, 12)

with col2:
    st.subheader("📦 Services & Billing")
    phone = st.selectbox("Phone Service", ["No", "Yes"])
    multiple = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    device = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
    tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
    movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["No", "Yes"])
    payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
    monthly = st.number_input("Monthly Charges", 0.0)
    total = st.number_input("Total Charges", 0.0)

st.divider()

# ---- Encode inputs ----
def encode_inputs():
    return np.array([[
        1 if gender == "Male" else 0,
        1 if senior == "Yes" else 0,
        1 if partner == "Yes" else 0,
        1 if dependents == "Yes" else 0,
        tenure,
        1 if phone == "Yes" else 0,
        ["No", "Yes", "No phone service"].index(multiple),
        ["DSL", "Fiber optic", "No"].index(internet),
        ["No", "Yes", "No internet service"].index(security),
        ["No", "Yes", "No internet service"].index(backup),
        ["No", "Yes", "No internet service"].index(device),
        ["No", "Yes", "No internet service"].index(tech),
        ["No", "Yes", "No internet service"].index(tv),
        ["No", "Yes", "No internet service"].index(movies),
        ["Month-to-month", "One year", "Two year"].index(contract),
        1 if paperless == "Yes" else 0,
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"].index(payment),
        monthly,
        total
    ]])

# ---- Prediction ----
if st.button("🔍 Predict Churn"):
    input_data = encode_inputs()
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = float(model.predict_proba(input_scaled)[0][1])  # <-- FIX float issue

    st.subheader("📈 Prediction Result")

    # ---- Risk Meter ----
    risk_percentage = int(probability * 100)
    st.progress(probability)  # works now

    # ---- Recommendation ----
    if probability > 0.7:
        st.error(f"⚠ High Churn Risk ({risk_percentage}%)")
        st.markdown("💡 **Recommendation:** Contact the customer immediately, offer discounts, retention plan, or incentives.")
    elif probability > 0.4:
        st.warning(f"⚠ Medium Churn Risk ({risk_percentage}%)")
        st.markdown("💡 **Recommendation:** Monitor the customer, offer loyalty programs or personalized plans.")
    else:
        st.success(f"✅ Low Churn Risk ({risk_percentage}%)")
        st.markdown("💡 **Recommendation:** Keep providing good service to maintain loyalty.")