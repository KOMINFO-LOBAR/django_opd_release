import os,sys
sys.path.append('/var/www/html/django_opd')
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_opd.settings')
application=get_wsgi_application()