#!/bin/bash/env sh

echo "Make Migrations"
python manage.py makemigrations

echo "Migrations"
python manage.py migrate

echo "Run server"
python manage.py runserver