#!/bin/bash
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Starting queue"
/usr/bin/supervisord &

# Start server
echo "Starting server"
gunicorn nessusEngine.wsgi:application --bind 0.0.0.0:8002