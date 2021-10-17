class Core():
    """
    Core server class 
    
    """
    #TODO: Do as mentioned below
        # Create a key pair for the core separetly using some other script
        # Store the public and private keys in different key files
        # Copy public key key file to the project root directory
        # keep the private key key file in core-server directory
        # Read the keys from the files whenever needed

    def __init__(self):
        self.nodes = {}
        self.candidates = {}
        self.block_creators = []
        self.unverified_transactions = []

    def register_node(self, key:str, address:str):
        self.nodes[key] = address

    #TODO: validate sign using key
    def valid_sign(self, sign:str, key:str):
        return True

    #TODO: validate sign from the data using key
    def create_sign(self, data:str, key:str):
        sign = ''

        return sign

    def add_candidate(self):
        pass

    def add_vote(self):
        pass

    def update_block_creators(self):
        pass

if __name__ == '__main__':
    pass
