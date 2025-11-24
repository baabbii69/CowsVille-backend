"""
WSGI config for FarmManagerSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use production settings if DJANGO_SETTINGS_MODULE is not set
settings_module = os.getenv(
    "DJANGO_SETTINGS_MODULE", "FarmManagerSystem.productions_settings"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
