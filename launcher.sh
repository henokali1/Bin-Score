#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Desktop/Bin-Score
python3 app.py
python3 serial_data.py
cd /
