from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import os, sys, struct
import argparse
import secrets


if sys.version_info >= (3, 8, 0):
        import time
        time.clock = time.process_time

from Database.keygenerator import *
keys = class_keys()
print(keys.AESkey)

