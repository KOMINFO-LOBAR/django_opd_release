_B='No respons from: '
_A='created: '
import logging,feedparser
from .models import info_hoax
logger=logging.getLogger()
def auto_get_hoax_issue():
	C='https://kominfo.go.id/content/rss/laporan_isu_hoaks'
	try:
		A=feedparser.parse(C)
		if A:
			if A.entries:
				for B in A.entries:
					E,D=info_hoax.objects.get_or_create(name=B.title,defaults={'link':B.link})
					if D:logger.error(_A+B.title)
	except:logger.error(_B+C);return False
	return True
def auto_get_widget():
	C='http://widget.kominfo.go.id/data/covid-19/gpr.xml'
	try:
		B=feedparser.parse(C)
		if B:
			if B.entries:
				for A in B.entries:
					E,D=info_widget.objects.get_or_create(title=A.title,defaults={'categori':A.categori,'publish_date':A.pubDate,'author':A.author,'link':A.link})
					if D:logger.error(_A+A.title)
	except:logger.error(_B+C);return False
	return True