#!/bin/bash

# Set the file extension to process
FILE_EXT="wav"

# Set the command to run on each file
PROCESS_CMD="python3 ./src/help.py"

file_count=0
# Function to process files and directories
process_files() {
    local src_dir="$1"
    local dest_dir="$2"

    # Loop through files and directories in the source directory
    for item in "$src_dir"/*; do
        if [ -d "$item" ]; then
            # If it's a directory, recursively call the function
            process_files "$item" "$dest_dir"
        elif [ -f "$item" ] && [ "${item##*.}" == "$FILE_EXT" ]; then
            $PROCESS_CMD "$item" "$dest_dir"

            # Increment the file count and display progress on the same line
            ((file_count++))
            progress=$((file_count * 100 / total_files))
            printf "\033[F"
            printf "\r\033[K"
            printf "\rProcessing %d out of %d files... \nProgress: [%-50s] %d%%" "$file_count" "$total_files" "$(< /dev/zero tr '\0' '=' | head -c $((progress / 2)))" "$progress"
        fi
    done
}

# Check if the root directory argument is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <root_directory> <output_file>"
    exit 1
fi

# Get the root directory from the command-line argument
root_dir="$1"

# Get the total number of files with the specified extension in the root directory
total_files=$(find "$root_dir" -type f | wc -l)
echo ""
# Process the input directory
process_files "$root_dir" "$2"
