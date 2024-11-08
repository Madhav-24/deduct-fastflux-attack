import hashlib
import json
from time import time
import csv

# Import necessary modules
from flask import Flask, jsonify

app = Flask(__name__)


# Blockchain class definition

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='1', proof=100)  # Genesis block

    def create_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []  # Clear current transactions
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1  # Index of the block that will hold this transaction

    def add_ip_addresses(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.new_transaction("system", "blockchain", row['FastFlex_IP'])  # Updated to match the column name

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Example usage:
blockchain = Blockchain()
blockchain.add_ip_addresses("FastFlex_IPs_Predictions.csv")

last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

blockchain.create_block(proof)

print("Blockchain:", blockchain.chain)


# Define a route to get the list of malicious IP addresses from the blockchain
@app.route('/get_malicious_ips', methods=['GET'])
def get_malicious_ips():
    # Assuming the list of malicious IPs is stored in the `malicious_ips` attribute of the blockchain object
    malicious_ips = blockchain.malicious_ips
    return jsonify({'malicious_ips': malicious_ips})

if __name__ == '__main__':
    app.run(debug=True, port=5002)

# Path: blockchain.py
