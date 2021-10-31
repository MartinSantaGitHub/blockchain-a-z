# region Libraries
import datetime
from flask import Flask, jsonify
from blockchain import Blockchain

# endregion

# region Mining a chainblock's block

# Create a Web App
app = Flask("foo")

# Create a Blockchain
blockchain = Blockchain()


# Mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    last_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, last_hash)

    response = {
        'message': 'Congrats, you just mined a new block!',
        'block': block
    }

    return jsonify(response), 201


# Get the complete blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain = blockchain.chain

    response = {
        'length': len(chain),
        'blockchain': chain
    }

    return jsonify(response), 200


# Validate the blockchain
@app.route('/is_valid', methods=['GET'])
def is_valid():
    response = {
        'is_valid': blockchain.is_chain_valid(),
        'timestamp': datetime.datetime.now()
    }

    return jsonify(response), 200


# Execute the web app
app.run(host='0.0.0.0', port=5000)

# endregion
