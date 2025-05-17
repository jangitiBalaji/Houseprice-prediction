import streamlit as st
import requests

st.title("🏡 Hyderabad House Price Prediction")

# User Inputs
area = st.number_input("Area in Sq. Ft.", min_value=100, max_value=10000, step=10)
bhk = st.number_input("Number of BHKs", min_value=1, max_value=10, step=1)
rate_persqft = st.number_input("Rate per Sq. Ft.", min_value=100, max_value=20000, step=100)

# Categorical inputs
location = st.selectbox("Location", ["Gachibowli", "Madhapur", "Kondapur", "Other"])
building_status = st.selectbox("Building Status", ["Ready to Move", "Under Construction"])

# Convert categorical to one-hot encoding
input_data = {
    "rate_persqft": rate_persqft,
    "area_insqft": area,
    "BHK": bhk,
    "location_" + location: 1,  # Set selected location
    "building_status_" + building_status: 1  # Set selected building status
}

# Make prediction
if st.button("Predict Price"):
    response = requests.post("http://127.0.0.1:5000/predict", json=input_data)
    
    if response.status_code == 200:
        st.success(f"🏠 Estimated House Price: ₹{response.json()['predicted_price(L)']} Lakhs")
    else:
        st.error("Error in prediction. Please try again.")


