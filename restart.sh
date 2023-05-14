#!/bin/bash

# update folder
git pull

# Stop the asebot.py process
pkill -f marsBot.py

# Start the asebot.py process
python3 ./marsBot.py &
