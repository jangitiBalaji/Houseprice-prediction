from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("house_price_model.pkl")

@app.route('/')
def home():
    return "House Price Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data as JSON
        data = request.json
        
        # Convert input data into a DataFrame
        df = pd.DataFrame([data])

        # Ensure input has the same feature structure as training data
        required_features = joblib.load("features.pkl")  # Load feature names
        df = df.reindex(columns=required_features, fill_value=0)  # Fill missing features with 0

        # Predict log price and convert back to original scale
        log_price_pred = model.predict(df)[0]
        price_pred = np.expm1(log_price_pred)  # Reverse log transformation
        
        return jsonify({'predicted_price(L)': round(price_pred, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
