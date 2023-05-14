#!/bin/bash

# Stop the asebot.py process
pkill -f asebot.py

# Start the asebot.py process
python3 ./asebot.py &
