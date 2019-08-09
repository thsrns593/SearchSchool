"""
WSGI config for searchSchool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application
sys.path.append('/opt/searchSchool')
sys.path.append('opt/SHIN/lib/python3.6/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "searchSchool.settings")

application = get_wsgi_application()
