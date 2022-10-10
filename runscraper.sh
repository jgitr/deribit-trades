#!/bin/bash

# Log Reboot
echo "$(date) rebooting scraper" >> reboot.txt

# Activate Python venv
source deribot/bin/activate
nohup /usr/local/bin/python3 main.py -V >> pv.txt 
