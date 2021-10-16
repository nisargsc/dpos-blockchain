# Blockchain for Dexter's Coffee shop
## About
This project is a blockchain implementation for coffee shop transactions. <br>
Each block in the blockchain stores list of verified transaction data. Other than data blocks also have num i.e. index of block, hash of the block, hash of the previous block, timestamp etc. Each transaction in the list has timestamp, customer name, amount, item name, and quantity fields. 

## Dependancies
This project uses `Flask` and `requests` libraries for distributed and decentralised implementation. <br> 
You can download this dependancies with `pip` using following commands
```
pip install Flask
```
```
pip install requests
```
To test the decentralised implementation you might need a HTTP client like [postman](https://www.postman.com/).
Run the following command in terminal to run a flask server . You can change the port number to run multiple nodes on seperate terminals. Make sure that you are in the project directory before runing the following.
```
flask run -p 5000
```

## Code Structure
This project is divided in 7 python files i.e. `block.py`, `blockchain.py`, `shop.py`, `transaction.py`, `main.py`, `app.py`, and `test.py`. Of this 7 files first 4 files have `Block`, `Blockchain`, `Shop`, `Transaction` classes respectivily. `main.py` is local implementation, a terminal based interface to interact with the blockchain. `test.py` is just a test file that creates few transactions and mines them to blockchain. `app.py` is the decentralised implementation, it is a flask api which can be used to interact with the blockchain.

### Block class
`Block` class has attributes like `num` : index of the block, `nonce` : number to be used in PoW, `data` : data of the block, `prev_hash` : hash of the previous block, `hash` : hash of the current block, `timestamp` : timestamp of the block creation, `prev` : previous block in the list, and `next` : next block in the list. <br>
And methods like `find_hash()` : Finds the hash for the current block using its contents, `update_hash()` : Updates the hash of the current block, `dict()` : Gives python dictionary representation of the current block, etc.

### Blockchain class
`Blockchain` class has attributes like `difficulty` : Difficulty level for mining new block, `genesis` : First block of the blockchain, and `head` : Latest block in the blockchain. <br>
And methods like `create_genesis()` : Creates the genesis block, `mine_block()` : Mines new blocks in the blockchain, `proof_of_work()` : Updates the nonce and hash according to the proof of work algorithm, `find_guess_hash()` : Finds guess hash to be used in the proof of work algoritm, `valid_proof()` : Validates if given hash satisfies proof of work condition, `varify_blocks()` : Varifies if given two block_dict make a valid blockchain or not, `valid_chain()` : Checks if given blockchain is valid or not, `update_chain()` : Updates the current blockchain with new given blockchain, `print()` : Prints the current blockchain in the terminal.

### Transaction class
`Transaction` class has attributes like `customer` : Name of the customer, `amount_paid` : Amount paid by the customer, `item` : Name of the item ordered, `quantity` : Quantity of the item ordered, `timestamp` : Timestamp of the transaction. <br>
And methods like `dict()` : Gives python dictionary representation of the transaction and `json()` : Gives json representation of the transaction.

### Shop class
`Shop` class has attributes like `unverified_transactions` : List of all the unverified transactions yet to be mined, `blockchain` : Blockchain of the transaction blocks, `block_list` : List representation of the blockchain, `nodes` : Set of neighbouring nodes in the network for the decentralised implementaion. <br>
And methods like `add_transaction()` : Adds new transaction to unverified transactions list, `mine_transactions()` : Mines all teh unverified transactions into a block, `register_node()` : Adds a new node to the set of neighbouring nodes for the decentralised implementation, and `resolve_conflicts()` : Consensus algoritm - Resolves conflict between nodes.

## Proof of Work and Consensus 
### Proof of work
We use proof of work algoritm in this project. SHA256 hash of the string `"{previous_block_nonce}{previous_block_hash}{current_block_nonce}"` should have its first `blockchain.difficulty` number of digit to be equal to `0`. We keep guessing the `current_block_nonce` until the above condition is satisfied. And then update the hash of the current block.
### Consensus
We resolve the conflicts between nodes by replacing the cureent blockchain with the logest valid blockchain in the network.
