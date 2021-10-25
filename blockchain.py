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

	def create_block(self, data):
		"""
		Creates new block

		:param data: <any> Data to store in the block. Can be of any type.

		:return: <dict> dict with the details of the block mined
		"""
		# Creating new block
		num = self.head.num + 1
		prev_hash = self.head.hash
		new_block = Block(num, data, prev_hash= prev_hash)

		# Seting the linked-list pointers
		new_block.prev = self.head
		self.head.next = new_block

		self.head = new_block

		return new_block.dict()

	def varify_blocks(self, prev_block:dict, block:dict, creator_key: str):
		"""
		Varifies if given two block_dict form valid blockchain or not.

		:param prev_block: <block_dict>
		:param block: <block_dict>
		:param creator_key: <str> public key of the block creator_key

		:return: <bool> True if valid False if not

		<block_dict> = {
			'num' : <int>,
			'timestamp' : <str>,
			'data' : <any>,
			'prev_hash' : <str>,
			'hash' : <str>,
			'sign' : <str>
		}
		"""

		if(creator_key==None):
			print("Creator key required")
			return False
		elif (not valid_sign(block['sign'], creator_key)):
			print("Sign invalid")
			return False

		# Checking if block has correct prev_hash and proof
		if(prev_block==None):
			return (block['prev_hash'] == None)
		else:
			return (prev_block['hash'] == block['prev_hash'])
				

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
			self.genesis = Block(new_chain[0]['num'], new_chain[0]['data'], timestamp= new_chain[0]['timestamp'])
			self.genesis.hash = new_chain[0]['hash']
			self.head = self.genesis
			for block_dict in new_chain[1:]:
				new_block = Block(block_dict['num'], block_dict['data'], block_dict['prev_hash'], timestamp= block_dict['timestamp'])
				new_block.prev = self.head
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
		b.create_block("This is Block " + str(i))
		print(b.head)

	print(b.varify_blocks(b.genesis.dict(),b.genesis.next.dict())) #True
	print(b.varify_blocks(b.genesis.dict(),b.head.dict())) #False
	print(b.varify_blocks(b.head.prev.dict(),b.head.dict())) #True
