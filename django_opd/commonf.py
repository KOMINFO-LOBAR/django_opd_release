from datetime import datetime,timedelta
from calendar import monthrange
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.utils.translation import ugettext as _
def get_natural_datetime(data_datetime):
	B=data_datetime;A=datetime.now();E=A-timedelta(hours=24);F=A-timedelta(hours=48);G=A-timedelta(days=7);H=A-timedelta(days=14);I=A-timedelta(days=21);J=A-timedelta(days=28);D=monthrange(A.year,A.month)[1];K=A-timedelta(days=D+1)
	if E<B<A:return naturaltime(B)
	elif F<B<A:return naturalday(B)
	elif G<B<A:return _(B.strftime('%A'))
	elif H<B<A:
		C=(A-B).days-7
		if C==0:return _('Seminggu yang lalu')
	elif I<B<A:
		C=(A-B).days-14
		if C==0:return _('Dua minggu yang lalu')
	elif J<B<A:
		C=(A-B).days-21
		if C==0:return _('Tiga minggu yang lalu')
	elif K<B<A:
		C=(A-B).days-D
		if C==0:return _('Sebulan yang lalu')
	return naturalday(B)