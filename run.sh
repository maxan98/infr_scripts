#!/bin/bash

#python vm_interactive.py && 
cat last-vm-info.txt | grep "IP" > IP.txt && cat last-vm-info.txt | grep 'IP\|Guest\|State\|Name' > 2info.txt && cat IP.txt | tr -dc '0-9.' > 2IP.txt && ./nparse.sh 2info.txt  > 2name.txt

