#!/bin/bash

# This script is used to run the application in the development environment.
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
