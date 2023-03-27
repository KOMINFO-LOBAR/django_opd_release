"""
WSGI config for django_opd project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

# di server tambahkan 2 baris ini
#import sys
#sys.path.append('/var/www/html/django_opd')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_opd.settings')

application = get_wsgi_application()
