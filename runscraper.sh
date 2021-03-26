#!/bin/bash

#while true; do
#    echo "rebooting scraper" >> reboot.txt
#    nohup python3 main.py -V > pv.txt 2>&1 
#    result=$?
#done &

echo "rebooting scraper" >> reboot.txt
nohup /usr/local/bin/python3 main.py -V > pv.txt 
