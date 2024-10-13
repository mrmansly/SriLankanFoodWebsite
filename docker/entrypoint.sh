#!/bin/bash
set -e

# Run migrations
python manage.py migrate

# Start the application (replace with your application start command)
exec "$@"