_A='Done'
from celery import shared_task
from django.core import management
from outbox_hitcount.hit_summary import auto_get_location,auto_hit_summary
from.data_cleanup import clean_unused_pages
from.data_fetch import auto_get_hoax_issue,auto_get_widget
@shared_task()
def session_cleanup():management.call_command('clearsessions',verbosity=0);print(_A);return _A
@shared_task()
def summary_hitcount(month_count=1):auto_hit_summary(month_count);print(_A);return _A
@shared_task()
def geo_location_hitcount(max_data=500):auto_get_location(max_data=max_data);print(_A);return _A
@shared_task()
def clean_unused_pages_():print('begin clean static pages');A=clean_unused_pages();print('end clean static pages');return A
@shared_task()
def auto_get_hoax_issue_():print('begin get hoax issue');A=auto_get_hoax_issue();print('end get hoax issue');return A
@shared_task()
def auto_get_widget_():print('begin get widget');A=auto_get_widget();print('end get widget');return A