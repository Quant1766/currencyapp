#!/bin/bash
python manage.py migrate
python manage.py makesuperuser
python manage.py update_currency