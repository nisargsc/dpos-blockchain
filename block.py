import hashlib
import datetime
import json

class Block():
    """
    Class for the blocks in the blockchain.

    :attr num: <int> Index of the block
    :attr nonce: <int> Nonce of the block. To be used in Proof of Work.
    :attr data: <any> Data to store in the block. Can be of any type.
    :attr prev_hash: <str> Hash of the previous block
    :attr hash: <str> Hash of the block
    :attr next: <Block> Next block in the chain
    :attr prev: <Block> Previous block in the chain
    :attr timestamp: <datetime object> Timestamp of the block

    :method find_hash(): Find the hash of the current block
    :method update_hash(): Updates the hash of the current block
    :method dict(): Returns the dict for the current block
    :method json(): Returns the json responce for the current block
    """

    def __init__(self, num:int, data, prev_hash=None):
        """
        :param num: <int> Index of the block
        :param data: <any> Data to store in the block. Can be of any type.
        :param prev_hash: <str> Hash of the previous block

        :return: None
        """
        self.num = num
        self.timestamp = datetime.datetime.now()
        self.nonce = 0
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.find_hash()
        self.next = None
        self.prev = None

    def find_hash(self):
        """
        Finds the hash of the current block using num, timestamp, data, prev_hash and nonce

        :return: <str> hash of the current block
        """
        hash = hashlib.sha256()
        block_string = f"{self.num}{str(self.timestamp)}{self.data}{self.prev_hash}{self.nonce}"
        hash.update(block_string.encode('utf-8'))
        return hash.hexdigest()

    def update_hash(self):
        """
        Updates the hash of the current block

        :return: None
        """
        self.hash = self.find_hash() 

    def dict(self):
        """
        :return: <dict> python dictionary for the current block details
        """
        block_dict = {
            'num' : self.num,
            'timestamp' : str(self.timestamp),
            'data' : self.data,
            'prev_hash' : self.prev_hash,
            'hash' : self.hash,
            'nonce' : self.nonce
        }
        return block_dict

    def json(self):
        """
        :return: <json> json responce for the current blcok details
        """
        block_json = json.dumps(self.dict(), indent = 4)
        return block_json

    def __str__(self):
        """
        Gets called every time block object is converted to string

        :return: <str> String of the json responce
        """
        return str(self.json())
        # return f"\n \
        # num : {self.num} \n \
        # timestamp : {self.timestamp} \n \
        # data : {self.data} \n \
        # prev_hash : {self.prev_hash} \n \
        # hash : {self.hash} \n \
        # nonce : {self.nonce} \n \"

if __name__ == '__main__':

    # Test

    block = Block(0,"genesis")
    print(block)

    print(block)
    block.data = "Genesis"
    block.update_hash()
    print(block)