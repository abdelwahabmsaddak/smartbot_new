#!/bin/bash
chmod +x backend/app.py
gunicorn backend.app:app --bind 0.0.0.0:$PORT
