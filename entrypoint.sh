#!/bin/bash
set -e

# Apply migrations
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable

# Create the admin superuser if it does not already exist
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() else exit(1)"; then
        python manage.py createsuperuser \
            --noinput \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL
        echo "Admin user $DJANGO_SUPERUSER_USERNAME created successfully."
    else
        echo "Admin user $DJANGO_SUPERUSER_USERNAME already exists."
    fi
else
    echo "Admin user $DJANGO_SUPERUSER_USERNAME not defined."
fi

if [ "$DEBUG" = "False" ]; then
    echo "Run collectstatic since DEBUG is False"
    python manage.py collectstatic --no-input --clear
fi

$@

#gunicorn --bind 0.0.0.0:8000 --workers 3 dressing.wsgi:application
