#!/bin/bash
set -e

# Apply migrations
python manage.py migrate
python manage.py makemigrations
python manage.py migrate

# Create the admin superuser if it does not already exist
cat create_admin.py | python manage.py shell

# Start the Django development server
python manage.py runserver 0.0.0.0:8000