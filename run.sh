#!/bin/bash
echo "Hello, I will fetch IP addresses and other stuff. Just insert some info about port-forwarding."
read -p 'dst-port: ' varname
read -p 'to-port: ' varname1
echo $varname | tr -dc '0-9'>dstport.txt
echo $varname1 | tr -dc '0-9' >toport.txt
#python vm_interactive.py && 
cat last-vm-info.txt | grep "IP" > IP.txt && cat last-vm-info.txt | grep 'IP\|Guest\|State\|Name' > 2info.txt && cat IP.txt | tr -dc '0-9.' > 2IP.txt && ./nparse.sh 2info.txt  > 2name.txt
python3 arg.py > mikrotik.conf
