class Core():
    """
    Core server class 
    
    """
    def __init__(self):
        self.nodes = {}
        self.candidates = {}
        self.block_creators = []

    def register_node(self, key, address):
        self.nodes[key] = address

    #TODO: validate sign using key
    def valid_sign(self, sign, key):
        return True

    def add_candidate(self):
        pass

    def add_vote(self):
        pass

    def update_block_creators(self):
        pass

if __name__ == '__main__':
    pass
