#!/bin/bash


#we submitted the original script to ChatGPT and among various implementation #recommendations we selected the following:
 
#a check to ensure that the jq command is available in the system
command -v jq &> /dev/null || { echo "the command jq is not available."; exit 1; }


#a check to verify that the series.json file exists
[ -f "series.json" ] || { echo "the file series.json does not exist."; exit 1; }


#the original core of the script
cat series.json | jq -r '. | [.id, .title, (.works | map(.books_count | tonumber) | add)] | @tsv' | sort -t $'\t' -k3,3nr | head -n 5 | awk -F '\t' 'BEGIN { printf "%-8s %-40s %-20s\n", "id", "title", "total_books_count"} { printf "%-8s %-40s %-20s\n", $1, $2, $3 }'