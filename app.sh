#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Desktop/Bin-Score
#chromium-browser --app=http://127.0.0.1:5000/ --start-fullscreen
#python3 serial_data.py
python3 app.py

cd /

