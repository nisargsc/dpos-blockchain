from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import hashlib


class Key():

    def __init__(self):
        self.private_key = RSA.generate(bits=1024)
        self.public_key = self.private_key.public_key()

        self.public_key_str = self.public_key.export_key().decode()
        self.private_key_str = self.private_key.export_key().decode()

        self.public_key_hash = find_hash(self.public_key_str)
        self.private_key_hash = find_hash(self.private_key_str)

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

    def make_key_files(self):
        with open('private_key.pem', 'w') as sk:
            sk.write(self.private_key_str)
        with open('public_key.pem', 'w') as pk:
            pk.write(self.public_key_str)


def find_hash(key):
    hash = hashlib.sha256()
    hash.update(key.encode('utf-8'))
    return hash.hexdigest()

def read_key_file(key_path):
    key = open(key_path, 'r').read()
    return key

def get_rsa_key(key):
    rsa_key = RSA.import_key(key)
    return rsa_key

def valid_sign(data:str, sign:str, key:str):
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
    k.make_key_files()
    # print(k.public_key_str)
    k1 = get_rsa_key(read_key_file(key_path='public_key.pem'))
    print(k1.export_key().decode())
    s = k.create_sign(data)
    check = k.valid_sign(data1, s)
    print(check)
