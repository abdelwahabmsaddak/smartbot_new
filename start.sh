#!/bin/bash
chmod +x start.sh
gunicorn backend.app:app --bind 0.0.0.0:$PORT
