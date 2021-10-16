import requests
from shop import Shop
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

s = Shop()

@app.route('/mine', methods=['GET'])
def mine():
    # Makig sure that we are on the longest valid chain before mining
    s.resolve_conflicts()

    # Minig the block
    if (len(s.unverified_transactions) >= 2):
        s.mine_transactions()
        message = 'Mining complete. All transactions mined successfully'
    else:
        message = 'You need at least 2 transactions to mine a block'

    # Clearing the unverified transaction list in all nodes
    neighbours = s.nodes
    for node in neighbours:
        r = requests.get(f'http://{node}/transaction/unverified/clear')
        if r.status_code != 200:
            return 'Error in Neighbour node', 400 

    response = {
        'message' : message,
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def show_chain():
    response = {
        'length' : len(s.block_list),
        'chain' : s.block_list,
    }

    return jsonify(response), 200

@app.route('/transaction/unverified', methods=['GET'])
def show_unverified():
    response = {
        'length' : len(s.unverified_transactions),
        'unverified_transactions' : s.unverified_transactions,
    }

    return jsonify(response), 200

@app.route('/transaction/unverified/clear', methods=['GET'])
def clear_unverified():
    s.unverified_transactions = []
    response = {
        'message' : 'Unvarified transactions list cleared'
    }

    return jsonify(response), 200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    # Resolving conflicts and updating the chain
    replaced = s.resolve_conflicts()

    if replaced:
        response = {
            'message' : 'Our chain got replaced with longest valid chain',
            'new_chain' : s.block_list, 
        }
    else:
        response = {
            'message' : 'Our chain is longest valid chain',
        }
    
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # Registering the neighbouring nodes in the network
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        s.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(s.nodes),
    }
    return jsonify(response), 201

@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    values = request.get_json()

    # Checking if all the required fields are in the request values
    required = ['customer', 'amount', 'item', 'quantity']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    customer = values['customer']
    amount = values['amount']
    item = values['item']
    quantity = values['quantity']

    # Checking the if request values are valid

    if (not isinstance(amount, (int, float))) or amount <= 0:
        return 'Amount should be a positive number', 400
    if (not isinstance(quantity, (int, float))) or quantity <= 0:
        return 'Quantity should be a positive number', 400
    if (not isinstance(customer, str)) or customer.isnumeric():
        return 'Customer name should be a non-numeric string', 400
    if (not isinstance(item, str)) or item.isnumeric():
        return 'Item name should be a non-numeric string', 400

    # Add transaction in current node
    t_dict = s.add_transaction(customer, amount, item, quantity)
    data = {
        't_dict' : t_dict,
    }

    # Adding the same transaction in other nodes
    neighbours = s.nodes
    for node in neighbours:
        r = requests.post(url= f'http://{node}/transaction/add_dict', json = data)
        if r.status_code != 201:
            return 'Error from the neighbour nodes', 400

    response = {
        'message' : 'Transaction is added to the unverified transactions list',
    }

    return jsonify(response), 201

@app.route('/transaction/add_dict', methods=['POST'])
def add_transaction_dict():
    data = request.get_json()
    print(data)

    s.unverified_transactions.append(data['t_dict'])

    response = {
        'message' : 'Transaction is added to the unverified transactions list',
    }

    return jsonify(response), 201

if __name__ == '__main__':
    app.run(debug=True)