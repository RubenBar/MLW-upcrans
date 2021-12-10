#!/bin/bash

echo "INSTALL DEPENDENCIES"

#TOR
apt-get -y install tor

#NMAP
apt-get -y install nmap

#CURL
apt-get -y install curl

#PIP
apt-get -y install python-pip

#CRYPTO
pip install pycrypto

#Tkinter
apt-get -y install python3-tk
