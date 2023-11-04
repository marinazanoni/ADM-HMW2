#!/bin/bash


#this bash script reads the series.json file and uses the jq command to extract information #from the file such as id,title and the total book count in the works section.
#the extracted data is then sorted based on the total book count in descending order.
#only the first 5 lines are selected using the head -n5 command.
#Finally, the data is formatted using the awk command to present the results in a table with aligned columns.


cat series.json | jq -r '. | [.id, .title, (.works | map(.books_count | tonumber) | add)] | @tsv' |
sort -t $'\t' -k3,3nr | head -n 5 | awk -F '\t' 'BEGIN { printf "%-8s %-40s %-20s\n", "id", "title",
 "total_books_count"} { printf "%-8s %-40s %-20s\n", $1, $2, $3 }'