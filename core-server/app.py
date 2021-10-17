from core import Core
from flask import Flask, jsonify, request

core = Core()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=['GET'])
def demo():
    response = {
        'message' : 'Core is runnig!!',
    }
    return jsonify(response), 200

# Registering and Showing Nodes

@app.route('/node/register', methods=['POST'])
def register_node():

    values = request.get_json()

    # Checking if all the required fields are in the request values
    required = ['key', 'address', 'sign']
    if not all(k in values for k in required):
        return jsonify({'message': 'Error: Values missing key, address and sign required'}), 400

    key = values['key']
    address = values['address']
    sign = values['sign']

    if (core.valid_sign(sign, key)):
        core.register_node(key, address)
        response = {
            'message': 'Your node has been added to the core server',
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Error: Sign is not valid',
        }
        return jsonify(response), 400

@app.route('/node/show', methods=['GET'])
def show_nodes():
    response = {
        'nodes' : core.nodes
    }
    return jsonify(response), 200

# Adding, Showing and Clearing unverified Transactions

@app.route('/transaction/add_dict', methods=['POST'])
def add_transaction_dict():
    data = request.get_json()
    print(data)

    core.unverified_transactions.append(data['t_dict'])

    response = {
        'message' : 'Transaction is added to the unverified transactions list',
    }

    return jsonify(response), 201

@app.route('/transaction/unverified', methods=['GET'])
def show_unverified():
    response = {
        'length' : len(core.unverified_transactions),
        'unverified_transactions' : core.unverified_transactions,
    }

    return jsonify(response), 200

@app.route('/transaction/unverified/clear', methods=['GET'])
def clear_unverified():
    core.unverified_transactions = []
    response = {
        'message' : 'Unverified transactions list cleared'
    }

    return jsonify(response), 200

def add_candidate():
    pass

def show_candidates():
    pass

def vote():
    pass

if __name__ == '__main__':
    app.run(port=4000)
