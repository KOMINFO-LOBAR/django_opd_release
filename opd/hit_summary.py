_P='version'
_O='name'
_N='hit_count'
_M='site_id'
_L='end_date'
_K='country'
_J='success'
_I='ip_address'
_H='param_os'
_G=False
_F=True
_E='platform'
_D='browser'
_C='none'
_B='city'
_A=None
import datetime,json,os,random,time
from datetime import timedelta
import httpagentparser,pytz,requests
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import FieldDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from hitcount.models import Hit
from outbox_hitcount.models import HitCount,HitBrowser,HitDevice,HitOS,HitLocation
from .common_date import add_months,get_last_day_of_month
def get_response(url,timeout=60):return requests.get(url,timeout=timeout)
def get_popen(url):return os.popen(url).read()
def get_geolocation_opt3(str_ip_address):
	B=f"http://ip-api.com/json/{str_ip_address}";A=get_response(B)
	if A:
		A=A.json()
		if _J not in A:return _A
		if _K not in A:return _A
		if _B not in A:return _A
		if A['status']==_J:return A[_K],A[_B]
	return _A
def get_geolocation_opt1(str_ip_address):
	C='country_name';D=f"curl https://ipapi.co/{str_ip_address}/json/";B=get_popen(D)
	if B:
		A=json.loads(B)
		if C not in A:return _A
		if _B not in A:return _A
		return A[C],A[_B]
	return _A
def get_geolocation_opt2(str_ip_address):
	B=f"http://ipwho.is/{str_ip_address}";A=get_response(B)
	if A:
		A=A.json()
		if _J not in A:return _A
		if _K not in A:return _A
		if _B not in A:return _A
		if A[_J]:return A[_K],A[_B]
	return _A
def get_geolocation_opt4(str_ip_address):
	C='countryName';D=f"curl http://api.db-ip.com/v2/free/{str_ip_address}";B=get_popen(D)
	if B:
		A=json.loads(B)
		if C not in A:return _A
		if _B not in A:return _A
		return A[C],A[_B]
	return _A
def correct_version(version):
	C='<-!->';A=version
	if A.strip():B=A.replace('(',C);B=B.replace(')',C);return B.split(C)[0]
	return A
def is_field_exists(model,field):
	A=model
	if A:
		try:
			for B in A._meta.get_fields():
				if not B.many_to_many and B.name==field:return _F
		except FieldDoesNotExist:return _G
	return _G
def get_or_set_browser(browser):
	A=browser;C=A.get(_O)if A else _A;B=A.get(_P)if A else _A
	if not C:C=_C
	if not B:B=_C
	B=correct_version(B);A,D=HitBrowser.objects.get_or_create(name=C,version=B);return A
def get_or_set_os(param_os):
	A=param_os;C=A.get(_O)if A else _A;B=A.get(_P)if A else _A
	if not C:C=_C
	if not B:B=_C
	B=correct_version(B);A,D=HitOS.objects.get_or_create(name=C,version=B);return A
def get_or_set_device(device):
	A=device;C=A.get(_O)if A else _A;B=A.get(_P)if A else _A
	if not C:C=_C
	if not B:B=_C
	B=correct_version(B);A,D=HitDevice.objects.get_or_create(name=C,version=B);return A
def get_or_set_location(ip_address):
	A=ip_address
	if not A:A=_C
	B,C=HitLocation.objects.get_or_create(ip_address=A);return B
def hitcount_insert_m2m_field(hit_count,browser,param_os,platform,ip_address):B=hit_count;A=get_or_set_browser(browser);B.hits_browser.add(A);A=get_or_set_os(param_os);B.hits_os.add(A);A=get_or_set_device(platform);B.hits_device.add(A);A=get_or_set_location(ip_address);B.hits_location.add(A)
def special_condition(object_pk,data):
	A=data;J=['artikel','berita','galery_video','galery_foto','halaman_statis','pengumuman','social_media']
	for K in J:
		H=_G;I=ContentType.objects.filter(model=K)
		if I:
			D=I.get().model_class()
			if is_field_exists(D,'site')and is_field_exists(D,'created_at'):H=_F
		if H:
			E=D.objects.filter(id=object_pk);B=_A;F=_A
			if E:B=E.get().site_id;F=E.get().created_at
			if B and F:
				C=Site.objects.filter(id=B)
				if C:C=C.get();L=ContentType.objects.get_for_model(C);G,M=HitCount.objects.get_or_create(content_type=L,object_pk=B,defaults={_L:F,_M:B});G.count+=1;A={_N:G,_D:A[_D],_H:A[_H],_E:A[_E],_I:A[_I]};hitcount_insert_m2m_field(**A);G.save()
		else:pass
@transaction.atomic
def do_summary(qs):
	R=0;U=qs.count()
	for C in qs:
		G=C.ip;S=C.user_agent;H=httpagentparser.detect(S);I=H.get(_E);J=H.get('os');K=H.get(_D);D=C.hitcount.object_pk;L=C.hitcount.content_type;M=C.created;R+=1;B=_A;N=L.model_class()
		if N:
			O=_G
			if is_field_exists(N,'site'):
				P=N.objects.filter(id=D)
				if P:B=P.get().site_id;O=_F
				else:pass
			else:pass
			if not O:E={_N:_A,_D:K,_H:J,_E:I,_I:G};special_condition(D,E)
		if B:
			F=Site.objects.filter(id=B)
			if F:F=F.get();T=ContentType.objects.get_for_model(F);A,Q=HitCount.objects.get_or_create(content_type=T,object_pk=B,defaults={_L:M,_M:B});A.count+=1;E={_N:A,_D:K,_H:J,_E:I,_I:G};hitcount_insert_m2m_field(**E);A.save()
		if B:A,Q=HitCount.objects.get_or_create(content_type=L,object_pk=D,defaults={_L:M,_M:B})
		else:A,Q=HitCount.objects.get_or_create(content_type=L,object_pk=D,defaults={_L:M,_M:_A})
		A.count+=1;E={_N:A,_D:K,_H:J,_E:I,_I:G};hitcount_insert_m2m_field(**E);A.save()
	clear_summary_qs(qs);return _F
def clear_summary_qs(qs):A=qs.count();qs.delete();
def auto_hit_summary(max_data=500):
	I=getattr(settings,'TIME_ZONE','UTC');C=pytz.timezone(I);J=getattr(settings,'HITCOUNT_KEEP_HIT_IN_DATABASE',{'days':30});K=timezone.now()-timedelta(**J);B=3;D=add_months(K,1);A=datetime.datetime(D.year,D.month,1)
	while B>0:
		A=add_months(A,-1);E=A.year;F=A.month;L=get_last_day_of_month(E,F);G=datetime.datetime(E,F,L,23,59,59);A=C.localize(A);G=C.localize(G);H=Hit.objects.filter(created__gte=A).order_by('-id')[:max_data]
		if not H:B-=1
		elif do_summary(H):B-=1
		else:return _G
	return _F
@transaction.atomic
def auto_get_location(request_per_minute=30,max_data=500):
	J='loc1';G=max_data;E=datetime.datetime.now();H=E+timedelta(minutes=1);K=HitLocation.objects.filter(Q(country=_A)|Q(city=_A))[:G];F=0;I=[1,2,3,4,5,6,7];B=J
	for D in K:
		F+=1;C=D.ip_address
		if F<=request_per_minute:
			A=get_geolocation_opt1(C);B=J
			if not A:A=get_geolocation_opt2(C);B='loc2'
			if not A:A=get_geolocation_opt3(C);B='loc3'
			if not A:A=get_geolocation_opt4(C);B='loc4'
			if not A:B=_C
			else:D.country=A[0];D.city=A[1];D.save();time.sleep(random.choice(I))
		else:
			while datetime.datetime.now()<H:time.sleep(random.choice(I))
			F=0;E=datetime.datetime.now();H=E+timedelta(minutes=1);