from celery import shared_task
from django.conf import settings
from django.core import management
from outbox_hitcount.hit_summary import auto_get_location,auto_hit_summary
@shared_task()
def session_cleanup():print('begin clear session');management.call_command('clearsessions',verbosity=0);print('end clear session');return True
@shared_task()
def summary_hitcount():print('begin summary hitcount');auto_hit_summary();print('end summary hitcount');return True
@shared_task()
def geo_location_hitcount():print('begin geo location');auto_get_location(max_data=1000);print('end geo location');return True