#!/bin/bash
set -e

# allow a bit of time for the vault to be unsealed successfully
sleep 5

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Start the application (replace with your application start command)
exec "$@"