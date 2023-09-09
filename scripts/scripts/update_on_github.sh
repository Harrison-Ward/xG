#!/bin/bash

# Change to the directory containing your Git repository
cd /Users/harrisonward/Desktop/CS/Git/xG/

# Add all changes to the Git staging area
git add datasets/23_24_premier_league_events.csv datasets/23_24_shotmaps.csv

# Commit the changes with a commit message
git commit -m 'Auto-commit changes to events and shotmaps datasets'

# Push the changes to the remote repository (e.g., origin)
git push origin main
