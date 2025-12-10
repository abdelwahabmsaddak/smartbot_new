#!/bin/bash
python3 backend/init_db.py
gunicorn -w 4 -b 0.0.0.0:10000 backend.app:app
