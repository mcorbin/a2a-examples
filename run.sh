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
python agents/architect.py &
python agents/developer.py &
python agents/reviewer.py &

# Run orchestrator agent
python agents/orchestrator.py &

# Wait for all background processes
wait