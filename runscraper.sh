#!/bin/bash

while true; do
    nohup python3 main.py >> test.out 
    result=$?
done &
