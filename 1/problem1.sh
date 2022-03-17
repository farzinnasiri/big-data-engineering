#!/bin/bash
# ./problem1.sh sample_dir
if [ ! -d "$1" ]; then
    echo "[-] directory does not exist."
    exit 1
fi;

max=0

for name in $(ls "$1" | xargs -n 1 basename);do 
    name_with_out_extenstion=$(echo ${name%.*})    
    length=${#name_with_out_extenstion}    
    if [ "$length" -gt "$max" ]; then  
	      max=$length
    fi; 
done;
echo $max;

