from flask import Flask, render_template, request, jsonify
import requests
from blockchain import Blockchain  # Import the Blockchain class directly
import joblib
import os
import block_malicious_ips  # Import the block_malicious_ips module

app = Flask(__name__)

# Load the trained model and vectorizer
model_path = 'rf_classifier_model.joblib'
vectorizer_path = 'tfidf_vectorizer.joblib'

if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    rf_classifier = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model loaded successfully.")
else:
    print("Error: Model files not found.")

# Example function to classify IP addresses
def classify_ip(ip_addresses):
    # ... (unchanged)
    # Replace this URL with your IP address classification API endpoint
    url = 'http://127.0.0.1:5000/classify'
    data = {'ip_addresses': ip_addresses}
    response = requests.post(url, json=data)
    return response.json()

# Function to add IP addresses to the blockchain module
def add_to_blockchain(ip_addresses):
    blockchain_url = 'http://127.0.0.1:5001/add_ip'  # Assuming blockchain module is running on port 5001
    data = {'ip_address': ip_addresses}
    response = requests.post(blockchain_url, json=data)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # ... (unchanged)
    # Handle image upload and extract IP address
    # Example: classify IP address
    ip_address = request.remote_addr
    classification_result = classify_ip([ip_address])

    # Example: check if fastflux attack detected
    fastflux_detected = False
    malicious_ips = []

    if 'predictions' in classification_result:
        predictions = classification_result['predictions']
        if any(prediction == 'bad' for prediction in predictions):
            fastflux_detected = True
            malicious_ips = [ip_address]

            # Generate CSV file with detected malicious IPs
            with open('FastFlex_IPs_Predictions.csv', 'w') as f:
                f.write('\n'.join(malicious_ips))

            # Add malicious IPs to blockchain
            add_to_blockchain(malicious_ips)

            # Print a message indicating the model is being used
            print("Model used to classify IP addresses.")

    return jsonify({'fastfluxDetected': fastflux_detected, 'maliciousIPs': malicious_ips})

# Add a route to get the list of malicious IPs from the blockchain
@app.route('/get_malicious_ips', methods=['GET'])
def get_malicious_ips():
    blockchain_url = 'http://127.0.0.1:5001/get_malicious_ips'  # Assuming blockchain module is running on port 5001
    response = requests.get(blockchain_url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
    print("Block malicious IPs module is running.")
