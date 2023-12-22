import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_opd.settings')
app=Celery('django_opd')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule={'periodic-clear-sessions':{'task':'opd.tasks.session_cleanup','schedule':crontab(minute=0,hour=0)}}