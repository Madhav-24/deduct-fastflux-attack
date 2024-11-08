from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Example function to classify IP addresses
def classify_ip(ip_addresses):
    # Replace this URL with your IP address classification API endpoint
    url = 'http://127.0.0.1:5000/classify'
    data = {'ip_addresses': ip_addresses}
    response = requests.post(url, json=data)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
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
            with open('malicious_ips.csv', 'w') as f:
                f.write('\n'.join(malicious_ips))

    return jsonify({'fastfluxDetected': fastflux_detected, 'maliciousIPs': malicious_ips})

if __name__ == '__main__':
    app.run(debug=True)
