#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <python_script>"
    exit 1
fi

# Check if the input file exists
if [ ! -f "$1" ]; then
    echo "Input file $1 not found"
    exit 1
fi

# Read each line from the input file and execute the Python script with each link
while IFS= read -r line; do
    python3 "$2" -a -v "$line"
done < "$1"

