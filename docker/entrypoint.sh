#!/bin/bash
set -e

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Start the application (replace with your application start command)
exec "$@"