from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)
    # Convert data into DataFrame
    input_data = pd.DataFrame(data, index=[0])
    # Make prediction
    prediction = model.predict(input_data)
    # Return the prediction as JSON
    return jsonify(prediction=prediction[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)