#!/bin/bash

echo "SCRIPT #WEBSERVER TOR"

#RUN TOR
service tor start


#VARIABLES
TOR_URL="62uxh4sdczcyr6tkndwy5mvr3xjhmobruq5vxymtzusddcew6deem2ad.onion"
TOR_PROXY="localhost:9050"
CURL_CMD="curl -s --socks5-hostname"
CURL_RETURN_CODE=0


#COMMAND
CURL_OUTPUT=`${CURL_CMD} ${TOR_PROXY} ${TOR_URL} 2> /dev/null` || CURL_RETURN_CODE=$?
echo "${CURL_OUTPUT}"


#LOOP
while  [ ${CURL_RETURN_CODE} -eq 0 ]
do
	echo "curl connection okey"
	CURL_OUTPUT=`${CURL_CMD} ${TOR_PROXY} ${TOR_URL} 2> /dev/null` || CURL_RETURN_CODE=$?

done

echo "curl connection fail"
echo "RUN UPCRANS"

