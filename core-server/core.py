import random
class Core():
    """
    Core server class 
    
    """
    def __init__(self):
        self.node_addr = {} # Dict with key:value == node_id : node_address
        self.node_pk = {} # Dict with node_id : node_public_key
        self.candidates = {} # Dict with key:values == candidate_id : vote_count
        self.block_creators = []
        self.prev_creator = None
        self.next_creator = None
        self.max_creator_number = 3
        self.unverified_transactions = []

    def register_node(self, id:str, key:str, address:str):
        self.node_addr[id] = address
        self.node_pk[id] = key

    def add_candidate(self, id):
        if(id not in self.candidates):
            self.candidates[id] = 0

    def add_vote(self, id):
        if id in self.candidates:
            self.candidates[id] += 1

    def get_node_addr(self, id):
        return self.node_addr[id]

    def update_block_creators(self):
        sorted_candidates = sorted(self.candidates, key= self.candidates.get, reverse=True)
        self.block_creators = sorted_candidates[:self.max_creator_number]

    def update_next_creator(self):
        next_index = 0
        # if(self.prev_creator is not None) and (self.prev_creator in self.block_creators[:-1]):
        #     prev_index = self.block_creators.index(self.prev_creator)
        #     next_index = prev_index + 1
        next_index = random.randint(0, len(self.block_creators)-1)
        self.next_creator =  self.block_creators[next_index]

    def update_prev_creator(self):
        self.prev_creator = self.get_next_creator()

if __name__ == '__main__':
    pass
