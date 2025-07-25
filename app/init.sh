#!/bin/bash
set -e

echo "[init.sh] Sleeping 20 seconds to let dependent services start..."
sleep 20s

echo "[init.sh] Current working directory: $PWD"

if [ -f /app/requirements.txt ]; then
    echo "[init.sh] Installing Python dependencies..."
    pip install --no-cache-dir -r /app/requirements.txt
else
    echo "[init.sh] No requirements.txt found."
fi

echo "[init.sh] Creating /app/home directory with open permissions..."
mkdir -p /app/home
chmod 777 /app/home

echo "[init.sh] init.sh execution completed"
