_A='Done'
from celery import shared_task
from django.core import management
from outbox_hitcount.hit_summary import auto_get_location,auto_hit_summary
from.data_cleanup import clean_unused_pages
from.data_fetch import auto_get_hoax_issue,auto_get_widget
@shared_task()
def session_cleanup():management.call_command('clearsessions',verbosity=0);print(_A);return _A
@shared_task()
def summary_hitcount(max_data=500):auto_hit_summary(max_data);print(_A);return _A
@shared_task()
def geo_location_hitcount(max_data=500):auto_get_location(max_data=max_data);print(_A);return _A
@shared_task()
def clean_unused_pages_():clean_unused_pages();print(_A);return _A
@shared_task()
def auto_get_hoax_issue_():auto_get_hoax_issue();print(_A);return _A
@shared_task()
def auto_get_widget_():auto_get_widget();print(_A);return _A