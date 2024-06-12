#!/bin/bash

# Check if the input file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 papers_list.txt"
    exit 1
fi

# Read the input file
input_file=$1

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "File not found: $input_file"
    exit 1
fi

# Create the "papers" directory if it does not exist
mkdir -p papers

# Download each paper with the specified name
while IFS= read -r line; do
    # Use read to split the line into URL and filename
    read -r url filename <<< "$line"

    # Check if both URL and filename are provided
    if [ -z "$url" ] || [ -z "$filename" ]; then
        echo "Invalid line: $line"
        continue
    fi

    # Download the file
    output_path="papers/$filename"
    echo "Downloading $url as $output_path..."
    wget -q -O "$output_path" "$url" || curl -s -o "$output_path" "$url"
    
    # Check if the download was successful
    if [ $? -eq 0 ]; then
        echo "Downloaded $filename successfully."
    else
        echo "Failed to download $filename."
    fi
done < "$input_file"

