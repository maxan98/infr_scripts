#!/bin/bash
string=$(cat $1 | grep Name | awk ' {print $4} ')	
echo "${string:1:${#string}-3}"
