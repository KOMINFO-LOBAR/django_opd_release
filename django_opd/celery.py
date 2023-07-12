_B='schedule'
_A='task'
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_opd.settings')
app=Celery('django_opd')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule={'session-cleanup-daily-midnight':{_A:'opd.tasks.session_cleanup',_B:crontab(minute=0,hour=0)},'summary-hitcount-daily-midnight':{_A:'opd.tasks.summary_hitcount',_B:crontab(minute=0,hour=1)},'summary-geo-location-daily-midnight':{_A:'opd.tasks.geo_location_hitcount',_B:crontab(minute=0,hour=4)},'clean-unused-pages-daily-midnight':{_A:'opd.tasks.clean_unused_pages_',_B:crontab(minute=30,hour=0)},'auto-get-hoax-issue-daily-twice':{_A:'opd.tasks.auto_get_hoax_issue_',_B:crontab(minute=0,hour='*/12')},'auto-get-widget-daily-twice':{_A:'opd.tasks.auto_get_widget_',_B:crontab(minute=0,hour='*/12')}}