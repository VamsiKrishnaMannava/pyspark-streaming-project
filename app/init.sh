#!/bin/bash

apt-get update && apt-get install -y curl
# Wait until Spark master UI is reachable
until curl -s http://localhost:8080 | grep -q "Spark Master"; do
  echo "Waiting for Spark to be ready..."
  sleep 5
done

echo "PWD="$PWD
pip install -r /app/requirements.txt
alias 'll=ls -ltrah'
mkdir -p /app/home
chmod 777 /app/home
echo "init.sh execution completed"