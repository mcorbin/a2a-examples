#!/bin/bash

# Check if honcho is installed
if ! command -v honcho &> /dev/null; then
    echo "honcho is not installed. Installing..."
    pip install honcho
fi

# Run all agents using honcho
honcho start