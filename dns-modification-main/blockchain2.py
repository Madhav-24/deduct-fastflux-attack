
from flask import Flask, jsonify, request
import hashlib
import json
from time import time

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
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
# Initialize the blockchain
blockchain = Blockchain()
print("Blockchain:", blockchain.chain)
# Define a route to check if the blockchain module is running
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({'status': 'Blockchain module is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
# Path: app.py
