#!/bin/bash

# Get the directory containing the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load the current ID and script path from the environment variable file
source "$SCRIPT_DIR/env_vars.sh"

# Run the Python script with the single command and the current ID
python3 "$SCRIPT_DIR/main.py" single --id $CURRENT_ID

# Increment the ID and save it back to the environment variable file
NEXT_ID=$((CURRENT_ID + 1))
echo "CURRENT_ID=$NEXT_ID" > "$SCRIPT_DIR/env_vars.sh"
echo "SCRIPT_DIR=$SCRIPT_DIR" >> "$SCRIPT_DIR/env_vars.sh"
