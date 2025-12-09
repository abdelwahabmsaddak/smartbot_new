#!/bin/bash
export PORT=${PORT:-5000}
export PYTHONPATH=.

# تشغيل Flask عبر gunicorn
gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
