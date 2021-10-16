from shop import Shop

s = Shop()

# To mine we need at least 2 transactions
s.mine_transactions()

# adding 2 transactions and mining the 1st block
s.add_transaction('customer1', 20, 'tea', 1)
s.add_transaction('customer2', 50, 'ice coffee', 1)
s.mine_transactions()
print('block-1 mined')

# adding more transactions and mining more blocks
s.add_transaction('customer3', 100, 'kitkat', 4)
s.add_transaction('customer4', 30, 'coffee', 1)
s.add_transaction('customer1', 20, 'tea', 1)
s.mine_transactions()
print('block-2 mined')

s.add_transaction('customer2', 50, 'ice coffee', 1)
s.add_transaction('customer3', 100, 'kitkat', 4)
s.add_transaction('customer4', 30, 'coffee', 1)
s.add_transaction('customer1', 20, 'tea', 1)
s.mine_transactions()
print('block-3 mined')

s.add_transaction('customer2', 50, 'ice coffee', 1)
s.add_transaction('customer3', 100, 'kitkat', 4)
s.add_transaction('customer4', 30, 'coffee', 1)
s.mine_transactions()
print('block-4 mined')

# printing the blockchian
s.blockchain.print()