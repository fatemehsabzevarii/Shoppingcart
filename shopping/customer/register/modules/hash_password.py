
from Crypto.Hash import HMAC, SHA3_512
# from Crypto.PublicKey import RSA


def hash_pass(password):
    with open("hash_private_key.pem", "r") as file:
        private_key = bytes(file.read(), 'utf-8')

    hash_password = HMAC.new(key=private_key, digestmod=SHA3_512, msg=password.encode('utf-8'))
    return hash_password.hexdigest()


if __name__ == "__main__":
    password = '654321'
    hash = hash_pass(password)
