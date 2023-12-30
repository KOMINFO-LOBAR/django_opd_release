_A='created: '
import logging,feedparser
from.models import info_hoax,info_widget
logger=logging.getLogger()
from django.db import transaction
@transaction.atomic
def auto_get_hoax_issue():
	C='https://kominfo.go.id/content/rss/laporan_isu_hoaks';A=feedparser.parse(C)
	if A:
		if A.entries:
			for B in A.entries:
				E,D=info_hoax.objects.get_or_create(name=B.title,defaults={'link':B.link})
				if D:logger.error(_A+B.title)
	return True
@transaction.atomic
def auto_get_widget():
	D='https://widget.kominfo.go.id/data/covid-19/gpr.xml';C=3
	while C>0:
		B=feedparser.parse(D)
		if B:
			if B.entries:
				C=0
				for A in B.entries:
					F,E=info_widget.objects.get_or_create(title=A.title,defaults={'categori':A.category,'publish_date':A.published,'author':A.author,'link':A.link})
					if E:logger.error(_A+A.title)
		else:print(f"res {B}");C-=1
	return True