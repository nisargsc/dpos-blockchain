class Core():
    """
    Core server class 
    
    """

    def __init__(self):
        self.nodes = {} # Dict with key:value == node_public_key : node_address
        self.candidates = {} # Dict with key:values == candidate_public_key : vote_count
        self.block_creators = []
        self.max_creator_number = 3
        self.unverified_transactions = []
        #TODO: read the private key from the file and 
        self.private_key = ''

    def register_node(self, key:str, address:str):
        self.nodes[key] = address

    def add_candidate(self, key):
        if(key not in self.candidates):
            self.candidates[key] = 0

    def add_vote(self, key):
        if key in self.candidates:
            self.candidates[key] += 1

    def update_block_creators(self):
        sorted_candidates = sorted(self.candidates, key= self.candidates.get, reverse=True)
        self.block_creators = sorted_candidates[:self.max_creator_number]

if __name__ == '__main__':
    pass
