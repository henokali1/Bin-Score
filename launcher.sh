#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/Bin-Score

# python3 serial_data.py & python3 app.py & chromium-browser --app=http://127.0.0.1:5000/ --start-fullscreen
#chromium-browser --app=http://127.0.0.1:5000/ --start-fullscreen
sudo python3 key_listner.py
#cd /
