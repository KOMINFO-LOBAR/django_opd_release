_B='schedule'
_A='task'
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_opd.settings')
app=Celery('django_opd')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone='Asia/Makassar'
app.conf.beat_schedule={'periodic-clear-sessions':{_A:'opd.tasks.session_cleanup',_B:crontab(minute=45,hour=0)},'periodic-summary-hitcount':{_A:'opd.tasks.summary_hitcount',_B:crontab(minute=0,hour='*/6')},'periodic-get-ip-location':{_A:'opd.tasks.geo_location_hitcount',_B:crontab(minute=30,hour='*/4')},'periodic-clear-unuse-pages':{_A:'opd.tasks.clean_unused_pages_',_B:crontab(minute=55,hour=0)},'periodic-get-hoax-issue':{_A:'opd.tasks.auto_get_hoax_issue_',_B:crontab(minute=5,hour='*/12')},'periodic-get-widget-info':{_A:'opd.tasks.auto_get_widget_',_B:crontab(minute=15,hour='*/12')},'periodic-get-weather':{_A:'opd.tasks.auto_get_weather_',_B:crontab(minute=0,hour=0,day_of_week=0)}}