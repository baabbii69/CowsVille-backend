#!/bin/bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=FarmManagerSystem.productions_settings
gunicorn FarmManagerSystem.wsgi:application --bind 0.0.0.0:8000
