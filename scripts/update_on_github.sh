#!/bin/bash

# Change to the directory containing your Git repository
cd /Users/harrisonward/Desktop/CS/Git/xG/

# Define a log file path
log_file="/Users/harrisonward/Desktop/CS/Git/xG/scripts/logs/updater.log"

# Function to log messages
log() {
    local message="$1"
    # Use the current date and time for the log entry
    local timestamp="$(date +'%Y-%m-%d %H:%M:%S')"
    
    echo "$timestamp: $message" >> "$log_file"
    
}
# Log a message
log "Starting the update_on_github.sh script"

# Add all changes to the Git staging area
git add datasets/\*

# Commit the changes with a commit message
git commit -m 'Auto-commit changes to the datasets'

# Push the changes to the remote repository (e.g., origin)
git push origin main

# Log another message
log "Script execution completed"

