from calendar import monthrange
from datetime import datetime,timedelta
from functools import lru_cache
import pytz
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.utils import timezone
from django.utils.translation import gettext as _
@lru_cache(100)
def get_natural_datetime(data_datetime):
	B=data_datetime;E=getattr(settings,'TIME_ZONE','UTC');M=pytz.timezone(E);A=timezone.now();F=A-timedelta(hours=24);G=A-timedelta(hours=48);H=A-timedelta(days=7);I=A-timedelta(days=14);J=A-timedelta(days=21);K=A-timedelta(days=28);D=monthrange(A.year,A.month)[1];L=A-timedelta(days=D+1)
	if F<B<A:return naturaltime(B)
	elif G<B<A:return naturalday(B)
	elif H<B<A:return _(B.strftime('%A'))
	elif I<B<A:
		C=(A-B).days-7
		if C==0:return _('Seminggu yang lalu')
	elif J<B<A:
		C=(A-B).days-14
		if C==0:return _('Dua minggu yang lalu')
	elif K<B<A:
		C=(A-B).days-21
		if C==0:return _('Tiga minggu yang lalu')
	elif L<B<A:
		C=(A-B).days-D
		if C==0:return _('Sebulan yang lalu')
	return naturalday(B)