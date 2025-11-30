#!/bin/bash
echo "Starting SmartBot Flask Server..."

# دخول مجلد backend
cd backend

# تشغيل السيرفر Flask
exec python3 app.py
