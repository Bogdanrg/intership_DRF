#!/bin/sh
echo "Starting"

python traiding_main/manage.py runserver 0.0.0.0:8000
exec "$@"