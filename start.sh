#!/bin/bash

python ./manage.py check
python ./manage.py makemigrations --no-input --force
python ./manage.py migrate --no-input --force
python ./manage.py runserver 0.0.0.0:8000