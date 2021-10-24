#TODO: Complete the following methods
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256

class Key():

    key_pair
    public_key

   def __init__(self):
        
   def create_key_pair(self):
        self.key_pair = RSA.generate(bits=1024)
        self.public_key = self.key_pair.public_key()
        print("this is your private key: store it safely\n")
        print(self.key_pair.export_key())

#TODO: make sign from the data using key
   def create_sign(self, data:str):
        hash = SHA256.new(data.encode("utf8"))
        signer = PKCS115_SigScheme(self.key_pair)
        sign = signer.sign(hash)
        return sign

#TODO: varify the sign using key
   def valid_sign(self, data:str, sign:str):
        hash = SHA256.new(data.encode("utf8"))
        verifier = PKCS115_SigScheme(self.key_pair.public_key())
        try: 
            (verifier.verify(hash, sign))
            return True
        except:
            return False

if __name__ == '__main__':
    k = key()
    k.generate_key_pair()
    data = "test"
    data1 = "compromised_data_test"
    s = k.create_sign(data)
    check = k.valid_sign(data1, s)
    print(check)


#TODO: add methods to do following
    # create keys
    # save the keys in seprate key files

#TODO: Do as mentioned below
        # Create a key pair for the core server
        # Save the public and private keys in different key files
        # Copy the public key key file to the project root directory
        # Copy the private key key file in core-server directory
        # Read the keys from the files whenever needed