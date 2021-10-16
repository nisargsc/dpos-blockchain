import datetime
import json


class Transaction():
    """
    Class for the transaction details

    :attr customer: <str> Name of the customer
    :attr amount_paid: <float> Amount paid by the customer
    :attr item: <str> Name of the item ordered by the customer
    :attr quantity: <int> Quantity of the item ordered by the customer
    :attr timestamp: <datetime object> Timestamp of the transaction

    :method dict(): returns the dict for the transaction
    :method json(): returns the json responce for the transaction
    """

    def __init__(self, customer:str, amount_paid:float, item:str, quantity:int):
        """
        :param customer: <str> Name of the customer
        :param amount_paid: <float> Amount paid by the customer
        :param item: <str> Name of the item ordered by the customer
        :param quantity: <int> Quantity of the item ordered by the customer

        :return: None
        """
        self.customer = customer
        self.amount_paid = amount_paid
        self.item = item
        self.quantity = quantity
        self.timestamp = datetime.datetime.now()

    def dict(self):
        """
        :return: <dict> python dictionary for the transaction details
        """
        transaction_dict = {
            'timestamp' : str(self.timestamp),
            'customer' : self.customer,
            'amount' : self.amount_paid,
            'item' : self.item,
            'quantity' : self.quantity
        }
        return transaction_dict

    def json(self):
        """
        :return: <json> json responce for the transaction details
        """
        transaction_json = json.dumps(self.dict(), indent=4)
        return transaction_json
        
    def __str__(self):
        """
        Gets called every time transaction object is converted to string

        :return: <str> String of the json responce
        """
        return str(self.json())
        # return f"\n \
        # timestamp : {self.timestamp} \n \
        # customer : {self.customer} \n \
        # amount paid (Rs.) : {self.amount_paid} \n \
        # item : {self.item} \n \
        # quantity : {self.quantity} "

if __name__ == '__main__':

    # Test

    t1 = Transaction('a',10,'late10',1)
    t2 = Transaction('b',40,'late20',2)
    t3 = Transaction('c',30,'late10',3)

    print(t1)
    print(t2)
    print(t3)