from crypto import valid_sign, get_rsa_key
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

@app.route('/nodes/register', methods=['POST'])
def register_node():

    values = request.get_json()

    # Checking if all the required fields are in the request values
    required = ['id','key', 'address', 'sign']
    if not all(k in values for k in required):
        return jsonify({'message': 'Error: Values missing key, address and sign required'}), 400

    id = values['id']
    key = values['key']
    address = values['address']
    sign = bytes.fromhex(values['sign'])
    valid_msg = 'This is valid public key'

    if (valid_sign(valid_msg, sign, key)):
        # print("sign valid")
        core.register_node(id, key, address)
        response = {
            'message': 'Your node has been added to the core server',
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Error: Sign is not valid',
        }
        return jsonify(response), 400


@app.route('/nodes/show', methods=['GET'])
def show_nodes():
    response = {
        'nodes' : core.node_addr
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

# Adding, Showing Candidates and Adding votes

@app.route('/candidate/add', methods=['POST'])
def add_candidate():
    data = request.get_json()

    if 'id' not in data:
        error_response = {
            'message' : 'Key is needed for the nomination'
        }
        return jsonify(error_response), 400

    core.add_candidate(data['id'])

    response = {
        'message' : 'Candidate added to the list',
    }

    return jsonify(response), 201

@app.route('/candidate/show', methods=['GET'])
def show_candidates():
    response = {
        'candidates' : core.candidates
    }
    return jsonify(response), 200

@app.route('/vote', methods=['POST'])
def add_vote():
    values = request.get_json()

    # Checking if all the required fields are in the request values
    required = ['vote', 'id', 'sign']
    if not all(k in values for k in required):
        error_response = {
            'message' : 'Missing values'
        }
        return jsonify(error_response), 400

    vote = values['vote']
    sign = values['sign']
    id = values['id']

    key = get_rsa_key(core.node_pk[id])

    if valid_sign(vote, sign, key):
        core.add_vote(vote)
        core.update_block_creators()

        response = {
            'message' : 'Vote added',
        }

        return jsonify(response), 201
    else:
        error_response = {
            'message' : 'Vote sign is invalid'
        }
        return jsonify(error_response), 400
   
# Showing all block creators, next block creator, prev block creator

@app.route('/creators', methods=['GET'])
def show_creators():
    response = {
        'length' : len(core.block_creators),
        'blcok_creators' : core.block_creators,
    }

    return jsonify(response), 200

@app.route('/creators/next', methods=['GET'])
def show_next_creator():
    response = {
        'next_creator' : core.next_creator,
        'creator_addr' : core.get_node_addr(core.next_creator)
    }

    return jsonify(response), 200

@app.route('/creators/prev', methods=['GET'])
def show_prev_creator():
    response = {
        'prev_creator' : core.prev_creator,
        'creator_addr' : core.get_node_addr(core.prev_creator)
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(port=4000)
