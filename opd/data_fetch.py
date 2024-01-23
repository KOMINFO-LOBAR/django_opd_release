_F='%d %B %Y %z'
_E='TIME_ZONE'
_D='created: '
_C='publish_date'
_B='link'
_A=True
import logging,feedparser,os
from.models import info_hoax,info_widget
import pytz
from django.conf import settings
import datetime
logger=logging.getLogger()
from django.db import transaction
import xmltodict
@transaction.atomic
def auto_get_hoax_issue():
	D='title';B="curl 'https://www.kominfo.go.id/content/rss/laporan_isu_hoaks' -H 'pragma: no-cache' -H 'dnt: 1' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: www.radarcupon.es' --compressed";E=os.popen(B).read()
	try:
		C=xmltodict.parse(E);print('dat',C)
		for A in C['rss']['channel']['item']:L,F=info_hoax.objects.get_or_create(name=A[D],defaults={_B:A[_B],_C:A['pubDate']})
		if F:logger.error(_D+A[D])
	except:logger.error('No respons from: '+B);return False
	G=info_hoax.objects.filter(publish_date_convert__isnull=_A)
	for A in G:
		if not A.publish_date:H=getattr(settings,_E,'UTC');I=pytz.timezone(H);J=datetime.datetime.now();K=datetime.datetime(J.year,1,1,tzinfo=I);A.publish_date=K.strftime(_F)
		A.save()
	return _A
@transaction.atomic
def auto_get_widget():
	D='https://widget.kominfo.go.id/data/latest/gpr.xml';C=3
	while C>0:
		B=feedparser.parse(D)
		if B:
			if B.entries:
				C=0
				for A in B.entries:
					K,E=info_widget.objects.get_or_create(title=A.title,defaults={'categori':A.category,_C:A.published,'author':A.author,_B:A.link})
					if E:logger.error(_D+A.title)
		else:print(f"res {B}");C-=1
	F=info_widget.objects.filter(publish_date_convert__isnull=_A)
	for A in F:
		if not A.publish_date:G=getattr(settings,_E,'UTC');H=pytz.timezone(G);I=datetime.datetime.now();J=datetime.datetime(I.year,1,1,tzinfo=H);A.publish_date=J.strftime(_F)
		A.save()
	return _A