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

def register_node():
    pass

def add_candidate():
    pass

def show_candidates():
    pass

def vote():
    pass

if __name__ == '__main__':
    app.run(port=4000)
