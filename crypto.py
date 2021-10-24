from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256


class Key():

    def __init__(self):
        self.private_key = RSA.generate(bits=1024)
        self.public_key = self.private_key.public_key()

        self.public_key_str = self.public_key.export_key().decode()
        self.private_key_str = self.private_key.export_key().decode()

    def create_sign(self, data:str):
        hash = SHA256.new(data.encode("utf8"))
        signer = PKCS115_SigScheme(self.private_key)
        sign = signer.sign(hash)
        return sign

    def valid_sign(self, data:str, sign:str):
        hash = SHA256.new(data.encode("utf8"))
        verifier = PKCS115_SigScheme(self.private_key.public_key())
        try:
            (verifier.verify(hash, sign))
            return True
        except:
            return False


def get_rsa_key(key):
    rsa_key = RSA.import_key(key)
    return rsa_key

def valid_sign(self, data:str, sign:str, key:str):
        hash = SHA256.new(data.encode("utf8"))
        rsa_key = get_rsa_key(key)
        verifier = PKCS115_SigScheme(rsa_key)
        try: 
            (verifier.verify(hash, sign))
            return True
        except:
            return False

if __name__ == '__main__':
    k = Key()
    data = "test"
    data1 = "compromised_data_test"
    print('key:', k.public_key_str)
    k1 = get_rsa_key(k.public_key_str)
    print('key:', k1.export_key().decode())
    s = k.create_sign(data)
    check = k.valid_sign(data1, s)
    print(check)


#TODO: add methods to do following
    # save the keys in seprate key files

#TODO: Do as mentioned below
        # Create a key pair for the core server
        # Save the public and private keys in different key files
        # Copy the public key key file to the project root directory
        # Copy the private key key file in core-server directory
        # Read the keys from the files whenever needed