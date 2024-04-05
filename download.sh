#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
    echo "Input file $1 not found"
    exit 1
fi

# Count the total number of lines in the input file
total_lines=$(wc -l < "$1")
counter=0

# Read each line from the input file and execute the Python script with each link
while IFS= read -r line; do
    counter=$((counter+1))
    echo "Downloading file $counter of $total_lines"
    python3 ./utils/download_song.py -a -v "$line"
done < "$1"


