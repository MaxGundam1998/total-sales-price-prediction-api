#Import necssary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

#Initialize the flask application
total_price_predictor_api = Flask("SuperKart Total Sales Predictor")

#Load the trained machine learning model
model = joblib.load("backend_files/superkart_price_predicition_model_v1_0.joblib")

#Define a route for the home page (GET request)
@total_price_predictor_api.get('/')
def home():
  """
  This function handles the GET requests to the root URL ('/') of the API.
  It returns a simple welcome message

  """

  return "Welcome to Super Kart Total Sales Predictor API"

#Define a route for making predictions (POST request)
@total_price_predictor_api.post('/v1/sales')
def predict_total_sales():
  """
  This function handles POST requests to the '/v1/sales' endpoint.
  It expects a JSON payload containing total price details and returns the predicted
  sales price as a JSON response.

  """

  product_data = request.get_json()

  #Extract relevant features from JSON data

  sample = {
    'Product_Weight': product_data['Product_Weight'],
    'Product_Allocated_Area': product_data['Product_Allocated_Area'],
    'Product_MRP': product_data['Product_MRP'],
    'Store_Age_Years': product_data['Store_Age_Years'],
    'Product_Sugar_Content': product_data['Product_Sugar_Content'],
    'Store_Size': product_data['Store_Size'],
    'Store_Location_City_Type': product_data['Store_Location_City_Type'],
    'Store_Type': product_data['Store_Type'],
    'Product_Type_Category': product_data['Product_Type_Category']
  }

  #Convert the extracted data into a Pandas Dataframe
  input_data = pd.DataFrame([sample])

  #Make prediction (get log_price)
  predicted_total_sales = model.predict(input_data)[0]

  #Convert Predicted sales total to Python float
  predicted_total_sales = round(float(predicted_total_sales), 2)

  return jsonify({'Predicted Total Sales (in dollars)': predicted_total_sales})

@total_price_predictor_api.post('/v1/salesbatch')
def predict_total_sales_batch():
  """
  This function handles the POST requests to the '/v1/salesbatch' endpoint.
  It expects a CSV file containing total price details and returns the predicted
  sales price as a JSON response.
  """

  file = request.files['file']

  input_data = pd.read_csv(file)

  predicted_total_sales = model.predict(input_data).tolist()

  product_ids = input_data['Product_Id'].tolist()
  output_dict = dict(zip(product_ids, predicted_total_sales))

  return output_dict

if __name__ == '__main__':
    total_price_predictor_api.run(debug=True)
