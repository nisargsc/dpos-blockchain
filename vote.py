import json

class Vote():

    def __init__(self, vote:str, id:str, sign):
        self.vote = vote
        self.id = id
        self.sign = sign

    def dict(self):
        """
        :return: <dict> python dictionary for the vote details
        """
        vote_dict = {
            'id' : self.id,
            'vote' : self.vote,
            'sign' : self.sign
        }
        return vote_dict

    def json(self):
        """
        :return: <json> json responce for the vote details
        """
        vote_json = json.dumps(self.dict(), indent=4)
        return vote_json
        
    def __str__(self):
        """
        Gets called every time vote object is converted to string

        :return: <str> String of the json responce
        """
        return str(self.json())
