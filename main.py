import json
from shop import Shop

s = Shop()

q = False
while(not q):

    print('\n--------------------------------')
    print('Hi Dexter!!... What do you want to do ?')
    print('add transaction (a) | mine a block (m) | show the blockchain (b) | show unverified transactions (ut) | quit (q)')
    action = input('choose your option : ')
    print('--------------------------------\n')

    if (action == 'a'): # add transaction
       #input customer name
        while True:
            customer = input('Name of the customer: ')
            try:
                temp = float(customer)
                print('Customer name can not be a number')
            except ValueError:
                break
        # input amount paid
        while True:
            try:
                amount = float(input('Amount paid: '))
                if(amount > 0):
                    break
                else:
                    print('Amount should be positive')
            except ValueError:
                print('Amount should be a number')
                continue
        # input item name
        while True:
            item = input('Name of the item: ')
            try:
                temp = float(item)
                print('Item name can not be a number')
            except ValueError:
                break
        # input quantity
        while True:
            try:
                quantity = int(input('Quantity: '))
                if(quantity > 0):
                    break
                else:
                    print('Quantity should be positive')
            except ValueError:
                print('Quantity should be an integer')
                continue

        s.add_transaction(customer,amount,item,quantity)
        print('\nTransaction Added')

    elif (action == 'm'): # mine a block
        if (len(s.unverified_transactions) >= 2):
            s.mine_transactions()
            print('Mining complete. All transactions mined successfully')
        else:
            print('You need at least 2 transactions to mine a block')

    elif (action == 'b'): # show the blockchain
        if (len(s.block_list) > 0):
            print(json.dumps(s.block_list, indent=4))
        else:
            print('Blockchain don\'t have any blocks.')

    elif (action == 'ut'): # show the unvarified transactions
        if (len(s.unverified_transactions) > 0):
            print(json.dumps(s.unverified_transactions, indent=4))
        else:
            print('No unverified transaction available. All transactions are verified and mined.')

    elif (action == 'q'): # quit
        q = True

    else:
        print('Please choose proper option')