#!/bin/bash

ip2int()
{
    local a b c d
    { IFS=. read a b c d; } <<< $1
    echo $(((((((a << 8) | b) << 8) | c) << 8) | d))
}

int2ip()
{
    local ui32=$1; shift
    local ip n
    for n in 1 2 3 4; do
        ip=$((ui32 & 0xff))${ip:+.}$ip
        ui32=$((ui32 >> 8))
    done
    echo $ip
}

network()
{
    local addr=$(ip2int $1); shift
    local mask=$((0xffffffff << (32 -$1))); shift
    int2ip $((addr & mask))
}

#List of all IPs of the target system
hostIPs=$(ip -o addr | awk '!/^[0-9]*: ?lo|link\/ether/ {print $4}')
for ip in $hostIPs 
do
	#Obtain the IP
	ipHost=`echo $ip | cut -d "/" -f1`
	#Obtain the mask
	maskHost=`echo $ip | cut -d "/" -f2`
	if ! [[ $ipHost =~ .*:.* ]]
	then
		#Obtain the network of IP
		networkHost=$(network $ipHost $maskHost)
		
		#Obtain all the available IP neighbour
		listIPPropagation=$(nmap $networkHost/$maskHost -sn | grep for | cut -d " " -f5)
		for ipPropagation in $listIPPropagation 
		do
			echo $ipPropagation
			#SEND GET REQUEST 
		done
	fi
done