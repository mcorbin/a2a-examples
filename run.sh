#!/bin/bash

# Function to handle cleanup on Ctrl+C
cleanup() {
    echo "Stopping all processes..."
    kill 0  # Kill all processes in the current process group
    exit
}

# Set up trap to catch Ctrl+C (SIGINT) and SIGTERM
trap cleanup SIGINT SIGTERM

# Run all specialized agents in background
python -m agents.architect &
python -m agents.developer &
python -m agents.reviewer &

# Run orchestrator agent
python -m agents.orchestrator &

# Wait for all background processes
wait