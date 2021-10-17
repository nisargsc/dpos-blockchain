class Core():
    """
    Core server class 
    
    """

    def __init__(self):
        self.nodes = {}
        self.candidates = {}
        self.block_creators = []
        self.unverified_transactions = []
        #TODO: read the private key from the file and 
        self.private_key = ''

    def register_node(self, key:str, address:str):
        self.nodes[key] = address

    def add_candidate(self):
        pass

    def add_vote(self):
        pass

    def update_block_creators(self):
        pass

if __name__ == '__main__':
    pass
