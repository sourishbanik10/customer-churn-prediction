Customer Churn Prediction System 📊

streamlit web app link
https://customer-churn-prediction-kwdommdenbvqtvitbizpui.streamlit.app/

Predict whether a telecom customer is likely to churn using machine learning — complete with interactive Streamlit dashboard.

Table of Contents

Demo

Features

Usage

Model Details

Contributing

License

Demo

Check out the live app here: Streamlit Link
 🌐

Features

Predict churn probability for telecom customers.

Interactive two-column dashboard:

Customer Info

Services & Billing

Risk meter visualizing churn probability.

Business recommendations based on risk level.

Netflix-style dark UI with:

Red accents & glowing buttons

Card-style layout for inputs

Black input text on white boxes for numeric fields

Uses XGBoost model for predictions.

Fully responsive & user-friendly interface.

Screenshots


Main dashboard with customer info & services inputs.


Churn probability & recommendations.

Tech Stack

Python 3.12

Streamlit — UI & deployment

XGBoost — Churn prediction model

scikit-learn — Data preprocessing & scaling

NumPy / Pandas — Data manipulation

Joblib — Model & scaler serialization


Features include:

Customer demographics (gender, senior citizen, dependents, etc.)

Contract & payment info

Services subscribed

Monthly & total charges

Evaluation metrics:

Accuracy ~80%

ROC-AUC ~0.85

F1-score optimized for minority class

