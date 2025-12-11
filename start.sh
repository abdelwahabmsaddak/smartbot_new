#!/bin/bash
echo "Running initialization..."
python3 backend/init_db.py

echo "Starting Gunicorn server..."
gunicorn backend.app:app --bind 0.0.0.0:$PORT --timeout 200
