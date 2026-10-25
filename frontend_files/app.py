import streamlit as st 
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

st.title("SuperKart Total Sales Predictor")

st.subheader("Online Prediction")

# Collect user input for SuperKart product and store features
product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=1.0,
    step=0.1
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.1,
    step=0.01
)

product_mrp = st.number_input(
    "Product MRP (Maximum Retail Price)",
    min_value=0.0,
    value=100.0,
    step=1.0
)

store_age_years = st.number_input(
    "Store Age (Years)",
    min_value=0,
    value=10,
    step=1
)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location_city_type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    ["Supermarket Type1", "Supermarket Type2", "Grocery Store"]
)

product_type_category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

# Convert user input into a Dataframe
input_data = pd.DataFrame([{
    'Product_Weight': product_weight,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Age_Years': store_age_years,
    'Product_Sugar_Content': product_sugar_content,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Type_Category': product_type_category
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
  response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])
  if response.status_code == 200:
    prediction = response.json()['Predicted Total Sales (in dollars)']
    st.success(f"Predicted Total Sales (in dollars): {prediction}")
  
  else:
    st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
  if st.button("Predict Batch", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={'file': uploaded_file})
    if response.status_code == 200:
      predictions = response.json()
      st.success("Batch prediction completed successfully!")
      st.write(predictions)
    else:
      st.error("Unable to connect to the prediction API.")
