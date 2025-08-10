from django.db import transaction
from opd.models import Weather
import os,json,locale
from datetime import datetime,timedelta
import pytz
from django.conf import settings
@transaction.atomic
def get_data_weather():
	M='img';L='kabkota';K='%Y-%m-%d';E='hari';N='curl https://mhews.bmkg.go.id/api/prakicu2?kec=501420';F=os.popen(N).read();print('result0',F)
	if F:
		O=json.loads(F);locale.setlocale(locale.LC_ALL,'id_ID');H=getattr(settings,'TIME_ZONE','UTC');P=pytz.timezone(H);B=datetime.now(pytz.timezone(H));I=B.strftime(K);G=B.strftime('%A');Q=int(B.strftime('%z')[:3]);J=1
		for A in O:
			if A[E]!=G:
				J+=1
				if J>7:break
				B=B+timedelta(days=1);I=B.strftime(K);G=B.strftime('%A')
			if A[E]==G:D=A['jam'];D=D.split(' ')[:1];D=D[0];C=datetime.strptime(f"{I} {D}",'%Y-%m-%d %H:%M');C=P.localize(C);C=C+timedelta(hours=Q);R,S=Weather.objects.get_or_create(tgl=C,defaults={'tgl':C,E:A[E],L:A[L],'kec':A['kecamatan'],'t':A['t'],'hu':A['hu'],'ws':A['ws'],'wd':A['wd'],'weather_info':A['weatherInfo'],M:A[M]})
			else:break
		return True
	return False