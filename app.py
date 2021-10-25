import requests
from shop import Shop
from crypto import read_key_file, get_rsa_key
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

s = Shop()
core_server = 'http://127.0.0.1:4000/'

core_key_path = 'core_public_key.pem'
core_key = get_rsa_key(read_key_file(key_path=core_key_path))

@app.route('/', methods=['GET'])
def demo():
    response = {
        'message' : 'Node is runnig!!',
    }
    return jsonify(response), 200

# Registerning  node to the core server

@app.route('/register', methods=['POST'])
def register():
    # Registering the node to the core server
    values = request.get_json()

    node_address = values.get('address')
    if node_address is None:
        error_response = {
            'message' : 'Error: Please Send valid address',
        }
        return jsonify(error_response), 400

    # print('addr:', node_address)
    id = s.key_pair.public_key_hash
    # print('id:', id)
    public_key = s.key_pair.public_key_str
    # print('pk:', public_key)
    sign = s.key_pair.create_sign('This is valid public key').hex()
    # print('sign:', sign)
    data = {
        'id' : id,
        'key' : public_key,
        'address' : node_address,
        'sign' : sign
    }

    r = requests.post(url= f'{core_server}/nodes/register', json = data)
    r_json = r.json()
    if r.status_code != 201:
        error_response = {
            'message' : 'Error in the core server',
            'error' : r_json['message']
        }
        return jsonify(error_response), 400

    response = {
        'message': 'Your node has been added to the core server',
    }
    return jsonify(response), 201

# Adding, Storing, Clearing unverified transactions

@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    values = request.get_json()

    # Checking if all the required fields are in the request values
    required = ['customer', 'amount', 'item', 'quantity']
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing values'}), 400

    customer = values['customer']
    amount = values['amount']
    item = values['item']
    quantity = values['quantity']

    # Checking the if request values are valid

    if (not isinstance(amount, (int, float))) or amount <= 0:
        error_response = {'message' : 'Amount should be a positive number'}
        return jsonify(error_response), 400
    if (not isinstance(quantity, (int, float))) or quantity <= 0:
        error_response = {'message' : 'Quantity should be a positive number'}
        return jsonify(error_response), 400
    if (not isinstance(customer, str)) or customer.isnumeric():
        error_response = {'message' : 'Amount should be a positive number'}
        return jsonify(error_response), 400
    if (not isinstance(item, str)) or item.isnumeric():
        error_response = {'message' : 'Customer name should be a non-numeric string'}
        return jsonify(error_response), 400

    # Add transaction in current node
    t_dict = s.add_transaction(customer, amount, item, quantity)
    data = {
        't_dict' : t_dict,
    }

    # Adding the same transaction in other nodes
    r = requests.post(url= f'{core_server}/transaction/add_dict', json = data)
    if r.status_code != 201:
        error_response = {
            'message' : 'Error in the core server'
        }
        return jsonify(error_response), 400

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

@app.route('/transaction/unverified', methods=['GET'])
def show_unverified():
    r = requests.get(url= f'{core_server}/transaction/unverified')
    r_json = r.json()
    if r.status_code != 200:
        error_response = {
            'message' : 'Error in the core server'
        }
        return jsonify(error_response), 400

    s.unverified_transactions = r_json['unverified_transactions']

    response = {
        'length' : len(s.unverified_transactions),
        'unverified_transactions' : s.unverified_transactions,
    }

    return jsonify(response), 200

@app.route('/transaction/unverified/clear', methods=['GET'])
def clear_unverified():
    r = requests.get(url= f'{core_server}/transaction/unverified/clear')
    if r.status_code != 200:
        error_response = {
            'message' : 'Error in the core server'
        }
        return jsonify(error_response), 400

    s.unverified_transactions = []
    response = {
        'message' : 'Unverified transactions list cleared'
    }

    return jsonify(response), 200

# Election Process

@app.route('/election/apply', methods=['GET'])
def election_apply():
    #TODO: get public key below
    public_key = 'public key of the node'
    data = {
        'key' : public_key
    }

    # Sending the public key to nominate for the election
    r = requests.post(url= f'{core_server}/transaction/add_dict', json = data)
    r_json = r.json()
    if r.status_code != 201:
        error_response = {
            'message' : 'Error in the core server',
            'error' : r_json['message']
        }
        return jsonify(error_response), 400
    
    response = {
        'message' : 'Nomination added to the candidates list',
    }

    return jsonify(response), 200

@app.route('/vote', methods=['POST'])
def add_vote():
    values = request.get_json()

    if 'vote' not in values:
        error_response = {
            'message' : 'Vote required'
        }
        return jsonify(error_response), 400

    vote_id = values['vote']
    #TODO: Do as below
    vote = vote_id # sign this
    public_key = '' # get key here

    v_dict = s.add_vote(vote, public_key)

    # Adding the vote to the core server
    r = requests.post(url= f'{core_server}/vote', json = v_dict)
    r_json = r.json()
    if r.status_code != 201:
        error_response = {
            'message' : 'Error in the core server',
            'error' : r_json['message']
        }
        return jsonify(error_response), 400

    response = {
        'message' : 'Vote added to the core server',
    }

    return jsonify(response), 201

# Block creation process

@app.route('/mine', methods=['GET'])
def mine():
    # Makig sure that we are on the longest valid chain before mining
    s.resolve_conflicts()

    # Getting unverified transactions from the core server
    r = requests.get(url= f'{core_server}/transaction/unverified')
    r_json = r.json()
    if r.status_code != 200:
        error_response = {
            'message' : 'Error: While requesting unverified transactions from core server'
        }
        return jsonify(error_response), 400

    s.unverified_transactions = r_json['unverified_transactions']

    # Minig the block
    if (len(s.unverified_transactions) >= 2):
        s.mine_transactions()
        message = 'Mining complete. All transactions mined successfully'
    else:
        message = 'You need at least 2 transactions to mine a block'

    # Clearing the unverified transaction list in core
    r = requests.get(url= f'{core_server}/transaction/unverified/clear')
    if r.status_code != 200:
        error_response = {
            'message' : 'Error: While tring to clear unverified transactinos in core server'
        }
        return jsonify(error_response), 400


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

if __name__ == '__main__':
    app.run()