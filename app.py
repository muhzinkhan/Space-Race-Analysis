import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load('rfc_model.pkl')

# Streamlit UI
st.title("Random Forest Classifier Prediction App")

# User inputs for prediction
st.write("Enter feature values to make a prediction:")

# Example: If your model expects 4 numerical features
feature_1 = st.number_input("Organisation", min_value=0.0, max_value=69.0, value=0.0)
feature_2 = st.number_input("Rocket Status", min_value=0.0, max_value=1.0, value=0.0)
feature_3 = st.number_input("Rocket", min_value=0.0, max_value=444.0, value=0.0)
feature_4 = st.number_input("Mission", min_value=0.0, max_value=6836.0, value=0.0)
feature_5 = st.number_input("Year", min_value=0.0, max_value=2024.0, value=0.0)
feature_6 = st.number_input("Month", min_value=0.0, max_value=12.0, value=0.0)
feature_7 = st.number_input("WeekofMonth", min_value=0.0, max_value=5.0, value=0.0)
feature_8 = st.number_input("DayofMonth", min_value=0.0, max_value=31.0, value=0.0)
feature_9 = st.number_input("DayOfWeek", min_value=0.0, max_value=6.0, value=0.0)
feature_10 = st.number_input("Hour", min_value=0.0, max_value=23.0, value=0.0)
feature_11 = st.number_input("Launch Pad", min_value=0.0, max_value=159.0, value=0.0)
feature_12 = st.number_input("Country", min_value=0.0, max_value=21.0, value=0.0)

# Convert inputs to a NumPy array
features = np.array([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8, feature_9, feature_10, feature_11, feature_12]])

# Predict button
if st.button("Predict"):
    prediction = model.predict(features)
    st.write(f"Prediction: {prediction[0]}")
