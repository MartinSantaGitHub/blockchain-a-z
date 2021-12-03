import datetime
from flask import Flask, jsonify, request
from santacoin import Blockchain
from uuid import uuid4

# Create a Web App
app = Flask("foo")

# Create the node's address in the port 5000
node_address = str(uuid4()).replace('-', '')

# Create a Blockchain
blockchain = Blockchain()


# Mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    last_block = blockchain.get_last_block()
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    last_hash = blockchain.hash(last_block)

    blockchain.add_transaction(sender=node_address, receiver='Kirill', amount=10)

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
        'chain': chain
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


# Add a new transaction to the blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        return 'Missing elements for the transaction', 400

    index = blockchain.add_transaction(sender=json['sender'], receiver=json['receiver'], amount=json['amount'])
    response = {
        'message': f'The transaction will be added to the block number #{index}'
    }

    return jsonify(response), 201


# region Decentralize the blocks' chains

# Connect new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        return 'There is no nodes to add', 400

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'All the nodes were connected. The Santa blockchain contains the next nodes in \'total_nodes\'',
        'total_nodes': list(blockchain.nodes)}

    return jsonify(response), 201


# Replace the chain for the longest one (if necessary)
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_replace = blockchain.replace_chain()

    if is_replace:
        response = {'message': 'The nodes had different chains, and they were all replaced for the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Everything OK. The chain in all the nodes is already the longest one.',
                    'current_chain': blockchain.chain}

    return jsonify(response), 200


# endregion

# Execute the web app
app.run(host='0.0.0.0', port=5002)
