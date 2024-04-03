#!/bin/bash

# Set the file extension to process
FILE_EXT="wav"

# Set the command to run on each file
PROCESS_CMD="./src/remove_noise.sh"

file_count=0
# Function to process files and directories
process_files() {
    local src_dir="$1"
    local dest_dir="$2"

    # Create the destination directory if it doesn't exist
    mkdir -p "$dest_dir"

    # Loop through files and directories in the source directory
    for item in "$src_dir"/*; do
        if [ -d "$item" ]; then
            # If it's a directory, recursively call the function
            process_files "$item" "$dest_dir/$(basename "$item")_clean"
        elif [ -f "$item" ] && [ "${item##*.}" == "$FILE_EXT" ]; then
            # If it's a file with the specified extension, run the command and copy the processed file
            processed_file="$(basename "${item%.*}")_clean.$FILE_EXT"
            $PROCESS_CMD "$item" "$dest_dir/$processed_file"

            # Increment the file count and display progress on the same line
            ((file_count++))
            progress=$((file_count * 100 / total_files))
            printf "\033[F"
            printf "\r\033[K"
            printf "\rProcessing %d out of %d files... \nProgress: [%-50s] %d%%" "$file_count" "$total_files" "$(< /dev/zero tr '\0' '=' | head -c $((progress / 2)))" "$progress"
        fi
    done
}

# Function to process the root directory
process_root_dir() {
    local root_dir="$1"
    local clean_dir="${root_dir}_clean"

    # Create the clean directory
    mkdir "$clean_dir"

    # Process files and directories in the root directory
    process_files "$root_dir" "$clean_dir"
}

# Check if the root directory argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <root_directory>"
    exit 1
fi

# Get the root directory from the command-line argument
root_dir="$1"
echo ""
# Get the total number of files with the specified extension in the root directory
total_files=$(find "$root_dir" -type f -name "*.$FILE_EXT"| wc -l)
# Process the input directory
process_root_dir "$root_dir"
