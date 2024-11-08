from flask import Flask
import threading
import time
import pandas as pd
from scapy.all import *

app = Flask(__name__)

# List to store incoming IP addresses
incoming_ips = []

# Function to capture incoming DNS request packets
def capture_dns_requests():
    # Define a callback function to handle captured packets
    def packet_callback(packet):
        if DNS in packet and packet[DNS].qr == 0:  # Check if it's a DNS request
            src_ip = packet[IP].src
            if src_ip not in incoming_ips:
                incoming_ips.append(src_ip)

    # Sniff DNS request packets and call the callback function for each packet
    sniff(filter="udp and port 53", prn=packet_callback)

# Start capturing DNS request packets in a separate thread
capture_thread = threading.Thread(target=capture_dns_requests)
capture_thread.start()

# Function to periodically write captured IPs to a CSV file
def write_to_csv():
    while True:
        if incoming_ips:
            df = pd.DataFrame({"Captured IPs": incoming_ips})
            df.to_csv("captured_ips.csv", index=False)
            print("Captured IPs written to captured_ips.csv")
            incoming_ips.clear()  # Clear the list after writing to CSV
        time.sleep(60)  # Write to CSV every minute

# Start writing captured IPs to CSV in a separate thread
csv_thread = threading.Thread(target=write_to_csv)
csv_thread.start()

# Route to test Flask server
@app.route('/')
def index():
    return 'Flask server is running.'

# Route to display captured IPs
@app.route('/captured_ips')
def captured_ips():
    return ', '.join(incoming_ips)

# Start Flask server on port 5000
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
