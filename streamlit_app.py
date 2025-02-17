import streamlit as st
import joblib
import numpy as np
import pandas as pd


# Load the trained model
model = joblib.load('rfc_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')
label_encoder = joblib.load('label_encoder.pkl')
feature_ranges = joblib.load("feature_ranges.pkl")

categorical_features_names = preprocessor["ordinal"].feature_names_in_
onehot_features_names = preprocessor["onehot"].feature_names_in_
numerical_features_names = preprocessor["passthrough"].feature_names_in_


# Streamlit App UI
st.set_page_config(page_title="Space Mission Launch Prediction", layout="wide")
st.title("🚀 Space Mission Launch Prediction")

st.markdown("> 👈 *Enter feature values in the sidebar to make a prediction*")

# Sidebar inputs for features
st.sidebar.header("Input Features")

features = {}
# Categorical Features
for feature_name, categories in zip(categorical_features_names, preprocessor["ordinal"].categories_):
    features[feature_name] = st.sidebar.selectbox(feature_name, categories)

features[onehot_features_names[0]] = st.sidebar.selectbox(
    onehot_features_names[0], 
    preprocessor["onehot"].categories_[0]
    )

# Numerical Features
for feature_name in numerical_features_names:
    features[feature_name] = st.sidebar.slider(
        feature_name, 
        min_value=feature_ranges[feature_name]["min"], 
        max_value=feature_ranges[feature_name]["max"], 
        value=feature_ranges[feature_name]["mean"],
        step=1
        )

input_data = pd.DataFrame(features, index=[0])

# Display feature values as a Dataframe
st.write("### Selected Features:")
st.dataframe(input_data, use_container_width=True, hide_index=True)

# Preprocess input
processed_input = preprocessor.transform(input_data)

# Prediction button
if st.button("🚀 Predict"):

    prediction = model.predict(processed_input)
    probability = model.predict_proba(processed_input)
    predicted_label = label_encoder.inverse_transform(prediction)

    st.success(f"**Prediction:** {predicted_label[0]}")
    st.write(f"**Confidence:** {probability.max():.2%}")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built with ❤️ by [*Muhzin Khan*](https://github.com/muhzinkhan)")
