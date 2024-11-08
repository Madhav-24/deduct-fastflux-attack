import requests
import subprocess

# Function to block IP addresses
def block_ip(ip):
    subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name="Blocked_IP"', 'dir=in', 'action=block', f'remoteip={ip}'])

# Function to retrieve and block malicious IP addresses
def block_malicious_ips():
    # Get malicious IPs from the blockchain endpoint
    blockchain_url = 'http://127.0.0.1:5002/get_malicious_ips'
    response = requests.get(blockchain_url)
    if response.status_code == 200:
        data = response.json()
        malicious_ips = data.get('malicious_ips', [])
        # Block each malicious IP
        for ip in malicious_ips:
            block_ip(ip)
            print(f"Blocked malicious IP: {ip}")
    else:
        print("Failed to retrieve malicious IPs from the blockchain.")

# Main function
def main():
    block_malicious_ips()

if __name__ == "__main__":
    main()







