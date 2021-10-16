from blockchain import Blockchain
from transaction import Transaction
from urllib.parse import urlparse
import requests

class Shop():
    """
    Class for the coffee shop

    :attr unverified_transactions: <list> Array of all the unverified transactions yet to be mined
    :attr blockchain: <Blockchain> Blockchian with block data as list of varified transactions
    :attr block_list: <list> Array for the blockchain. with block_dict as elements
    :attr nodes: <set> Set of nodes for the decentralised implemetation

    :method add_transaction(): Adds new transactions to unverified_transactions list
    :method mine_transactions(): Mines all the transactions from the unverified_transactions list into a block
    :method register_nodes(): Add a new node to the set of nodes for decentralised implementation
    :method resolve_conflicts(): Consensus algoritm. Resolves conflicts by replacing the chain with longest valid chain in the network.
    """
    def __init__(self):
        """
        :return: None
        """
        self.unverified_transactions = []
        self.blockchain = Blockchain()
        self.block_list = []
        self.block_list.append(self.blockchain.genesis.dict())
        self.nodes = set()

    def add_transaction(self, customer:str, amount_paid:float, item:str, quantity:int):
        """
        Adds new transactions to unverified_transactions list

        :param customer: <str> Name of the customer
        :param amount_paid: <float> Amount paid by the customer
        :param item: <str> Name of the item ordered by the customer
        :param quantity: <int> Quantity of the item ordered by the customer

        :return: <dict> dict for the transaction details
        """
        t = Transaction(customer, amount_paid, item, quantity)
        self.unverified_transactions.append(t.dict())
        return t.dict()

    def mine_transactions(self):
        """
        Mines all the transactions from the unverified_transactions list into a block and resets the list

        :return: None
        """
        if (len(self.unverified_transactions) >= 2):
            block_dict = self.blockchain.mine_block(self.unverified_transactions)
            self.block_list.append(block_dict)
            self.unverified_transactions = []
        else:
            print('You need at least 2 transactions to mine a block')

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: <str> Address of node. Eg. 'http://127.0.0.1:5000/'

        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: <bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.block_list)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.blockchain.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.block_list = new_chain
            self.blockchain.update_chain(new_chain)
            return True

        return False

if __name__ == '__main__':

    # Test
    
    s = Shop()

    for i in range(5):
        for j in range(2):
            s.add_transaction('customer', 10, 'item', 6)
        s.mine_transactions()
    s.blockchain.print()
