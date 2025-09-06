#!/bin/bash

# Simple PDF Converter Script
# Usage: ./convert_to_pdf.sh input.html [output.pdf]

if [ $# -eq 0 ]; then
    echo "Usage: $0 input.html [output.pdf]"
    echo "If output.pdf is not specified, it will use the same name as input with .pdf extension"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.html}.pdf}"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Use the Node.js converter
echo "Converting $INPUT_FILE to $OUTPUT_FILE..."
node "$SCRIPT_DIR/html_to_pdf_converter.js" "$INPUT_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Conversion successful!"
    echo "PDF saved to: $OUTPUT_FILE"
    ls -lh "$OUTPUT_FILE"
else
    echo "❌ Conversion failed!"
    exit 1
fi