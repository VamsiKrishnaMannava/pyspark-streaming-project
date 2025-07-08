#!/bin/bash

echo "PWD="$PWD
pip install -r /app/requirements.txt
alias 'll=ls -ltrah'
mkdir -p /app/home
chmod 777 /app/home
