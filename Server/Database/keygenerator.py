import secrets
from Crypto.PublicKey import RSA

class class_keys:
    def __init__(self):
        self.AESkey = secrets.token_bytes(32)

        RSAkey = RSA.generate(2048)
        self.PUBLIC_RSAKEY = RSAkey.publickey().exportKey("PEM")
        self.PRIVATE_RSAKEY = RSAkey.exportKey("PEM")
