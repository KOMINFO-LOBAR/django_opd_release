_B='schedule'
_A='task'
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_opd.settings')
app=Celery('django_opd')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule={'periodic-clear-sessions':{_A:'opd.tasks.session_cleanup',_B:crontab(minute=0,hour=0)},'periodic-summary-hitcount':{_A:'opd.tasks.summary_hitcount',_B:crontab(minute=0,hour=1)},'periodic-get-ip-location':{_A:'opd.tasks.geo_location_hitcount',_B:crontab(minute=0,hour='*/6')}}