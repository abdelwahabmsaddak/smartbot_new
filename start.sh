#!/bin/bash

export PYTHONPATH=.
export PORT=${PORT:-5000}

# Initialize the database if needed
python3 backend/init_db.py

# Run Gunicorn server
gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
