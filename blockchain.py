import hashlib
import json
from block import Block

class Blockchain():
    """
    Class for the blockchain

    :attr difficulty: <int> Difficulty level for mining neew block
    :attr genesis: <Block> First block of the blockchain
    :attr head: <Block> Latest block in the blockchain

    :method create_genesis(): Creates the genesis block
    :method mine_block(): Mines new block in the blockchain
    :method proof_of_work(): Updates the nonce and hash of the block according to the proof of work algoritm
    :method find_guess_hash(): Finds hash for the guesss to be used in proof of work algoritm
    :method valid_proof(): Checks if the block has valid proof or not
    :method varify_blocks(): Varifies if given two block_dict form valid blockchain or not.
    :method valid_chain(): Determines if a given blockchain <list> is valid
    :method update_chain(): Updates the blockchain with new given blockchain <list>
    :method print(): Prints the blockchain
    """

    def __init__(self):
        """
        :return: None
        """
        self.difficulty = 4
        self.genesis = None
        self.create_genesis()
        self.head = self.genesis

    def create_genesis(self):
        """
        Creates the genesis block

        :return: None
        """
        self.genesis = Block(0, "Genesis")
        self.proof_of_work(self.genesis)
    
    def mine_block(self, data):
        """
        Mines new block

        :param data: <any> Data to store in the block. Can be of any type.

        :return: <dict> dict with the details of the block mined
        """
        # Creating new block
        num = self.head.num + 1
        prev_hash = self.head.hash
        new_block = Block(num, data, prev_hash)

        # Seting the linked-list pointers and applying proof_of_work()
        new_block.prev = self.head
        self.proof_of_work(new_block)
        self.head.next = new_block

        self.head = new_block

        return new_block.dict()
    
    def proof_of_work(self, block:Block):
        """
        Updates the nonce and the hash of the block according to the proof of work algoritm

        :param block: <Block>

        :return: None
        """
        while self.valid_proof(self.find_guess_hash(block)) is False:
            block.nonce += 1
        block.update_hash()
        
    
    def find_guess_hash(self, block:Block):
        """
        Finds hash for the guesss to be used in proof of work algoritm

        :param block: <Block>

        :return: <str> hash for the guess using prev_nonce, prev_hash, and nonce
        """
        if (self.genesis == None or self.genesis == block):
            guess = f"0g3N3s1Sbl0ck{block.nonce}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
        else:
            prev_nonce = block.prev.nonce
            prev_hash = block.prev.hash
            guess = f"{prev_nonce}{prev_hash}{block.nonce}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash

    def valid_proof(self, hash):
        """
        Validates the proof according to the proof of work algoritm

        :param hash: <hash> Hash generated for proof of work algoritm

        :return: <bool> True if guess_hash has its fist 'self.difficulty' digits as '0'.
        """
        return hash[:self.difficulty]=="0" * self.difficulty

    def varify_blocks(self, prev_block:dict, block:dict):
        """
        Varifies if given two block_dict form valid blockchain or not.
        To be used for consensus in decentralised implementation

        :param prev_block: <block_dict>
        :param block: <block_dict>

        :return: <bool> True if valid False if not

        <block_dict> = {
            'num' : <int>,
            'timestamp' : <str>,
            'data' : <any>,
            'prev_hash' : <str>,
            'hash' : <str>,
            'nonce' : <int>
        }
        """
        # Check if block has correct hash
        block_hash = hashlib.sha256( \
            f"{block['num']}{block['timestamp']}{block['data']}{block['prev_hash']}{block['nonce']}".encode()).hexdigest()
        if (block_hash != block['hash']):
            return False

        prev_block_hash = hashlib.sha256( \
            f"{prev_block['num']}{prev_block['timestamp']}{prev_block['data']}{prev_block['prev_hash']}{prev_block['nonce']}".encode()).hexdigest()
        if (prev_block_hash != prev_block['hash']):
            return False

        # Checking if block has correct prev_hash and proof
        if(prev_block==None):
            # print("if")
            proof_hash = hashlib.sha256(f"0g3N3s1Sbl0ck{block['nonce']}")
            # print(proof_hash)
            # print("(not self.valid_proof(proof_hash)): ", (not self.valid_proof(proof_hash)))
            if (block['prev_hash'] != None) or (not self.valid_proof(proof_hash)):
                return False
            else:
                return True
        else:
            # print("else")
            proof_hash = hashlib.sha256(f"{prev_block['nonce']}{prev_block['hash']}{block['nonce']}".encode()).hexdigest()
            # print(proof_hash)
            # print("(prev_block['hash'] != block['prev_hash']): ", (prev_block['hash'] != block['prev_hash']))
            # print("(not self.valid_proof(proof_hash)): ", (not self.valid_proof(proof_hash)))
            if (prev_block['hash'] != block['prev_hash']) or (not self.valid_proof(proof_hash)):
                return False
            else:
                return True

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain in python list (array) form i.e. self.block_list

        :return: <bool> True if valid, False if not
        """
        prev_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if (not self.varify_blocks(prev_block,block)):
                print(f'{json.dumps(prev_block, indent=4)}')
                print(f'{json.dumps(block, indent=4)}')
                print("-----^^Not valid blocks^^------")
                return False
            prev_block = block
            current_index += 1

        return True
    
    def update_chain(self, new_chain:list):
        """
        Updates the chain using new_chain which is list of block_dict
        To be used for consensus in decentralised implementation

        :param new_chain: <list> list of block_dict

        :return: None
        """
        if self.valid_chain(new_chain):
            self.genesis = None
            self.genesis = Block(new_chain[0]['num'], new_chain[0]['data'])
            self.genesis.nonce = new_chain[0]['nonce']
            self.genesis.hash = new_chain[0]['hash']
            self.genesis.timestamp = new_chain[0]['timestamp']
            self.head = self.genesis
            for block_dict in new_chain[1:]:
                new_block = Block(block_dict['num'], block_dict['data'], block_dict['prev_hash'])
                new_block.prev = self.head
                new_block.nonce = block_dict['nonce']
                new_block.timestamp = block_dict['timestamp']
                self.head.next = new_block
                self.head = new_block

    def print(self):
        """
        Prints the blockchain

        :return: None
        """
        temp = self.genesis
        while(temp != None):
            print(temp)
            temp = temp.next

if __name__ == '__main__':

    # Test

    b = Blockchain()

    print(b.head)
    for i in range(10):
        b.mine_block("This is Block " + str(i))
        print(b.head)

    print(b.varify_blocks(b.genesis.dict(),b.genesis.next.dict())) #True
    print(b.varify_blocks(b.genesis.dict(),b.head.dict())) #False
    print(b.varify_blocks(b.head.prev.dict(),b.head.dict())) #True
