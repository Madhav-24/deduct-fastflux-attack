from scapy.all import *
import threading
import time
import random
import csv

# List to store incoming IP addresses
incoming_ips = []

# Function to capture incoming DNS request packets
def capture_dns_requests(packet):
    if DNS in packet and packet[DNS].qr == 0:  # Check if it's a DNS request
        src_ip = packet[IP].src
        if src_ip not in incoming_ips:
            incoming_ips.append(src_ip)

# Start capturing DNS request packets
def start_packet_capture():
    sniff(filter="udp and port 53", prn=capture_dns_requests, store=0)

# Function to write captured IPs to a CSV file
def write_to_csv():
    with open('captured_ips.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Captured IPs'])
        for ip in incoming_ips:
            writer.writerow([ip])
    print("Captured IPs written to captured_ips.csv")

# Start capturing DNS request packets in a separate thread
capture_thread = threading.Thread(target=start_packet_capture)
capture_thread.start()

# Start sending DNS response packets
def send_dns_responses():
    while True:
        for ip in incoming_ips:
            target_ip = "127.0.0.1"  # Destination IP address
            print(f"Generated IP: {ip}")  # Print generated IP
            dns_response = IP(dst=target_ip)/UDP()/DNS(id=random.randint(1, 65535), qr=1, an=DNSRR(rrname="example.com", rdata=ip))
            send(dns_response, verbose=False)  # Send the packet
        time.sleep(0.1)  # Adjust the frequency of responses as needed

dns_thread = threading.Thread(target=send_dns_responses)
dns_thread.start()

# Write captured IPs to CSV file every minute
while True:
    time.sleep(60)
    write_to_csv()
