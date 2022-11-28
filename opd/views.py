_t='opd/search-result.html'
_s='opd/detail.html'
_r='photo__berita__id'
_q='berita__id'
_p=False
_o='num_pages'
_n='jumlah'
_m='page_obj'
_l='page'
_k='-view_count'
_j='menu'
_i='body'
_h='date2'
_g='date1'
_f='artikel'
_e='pengumuman'
_d='-updated_at'
_c='deskripsi'
_b='isi_berita'
_a='kategori__nama'
_Z='nama'
_Y=True
_X='feed1'
_W='?page=1'
_V='/search/'
_U='berita'
_T='photo__file_path'
_S='name'
_R='POST'
_Q='updated_at'
_P='size'
_O='jenis'
_N='/admin'
_M="Domain <b>%s</b> belum terdaftar, silahkan hubungi <br><a href='%s'>admin</a><br> untuk melakukan pendaftaran"
_L='account/error404.html'
_K='msg'
_J='admin__username'
_I='judul_seo'
_H='site__name'
_G='judul'
_F='feed2'
_E='search'
_D='-id'
_C='id'
_B=None
_A='created_at'
from urllib.parse import urlsplit
import calendar,datetime,re,feedparser
from account.commonf import get_topFoto
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import OuterRef,Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.utils.functional import empty
from django.utils.html import strip_tags
from django.utils.safestring import SafeString
from django.utils.text import Truncator,slugify
from django_opd.commonf import get_natural_datetime
from hitcount.models import Hit,HitCount
from hitcount.views import HitCountMixin
from humanize import naturalsize
from opd.models import comment
from .  import menus
from .forms import CommentForm
from .models import *
cache_item=dict()
cache_item[_X]=_B
cache_item[_g]=_B
cache_item[_F]=_B
cache_item[_h]=_B
def get_siteID(request):
	siteID=Site.objects.filter(domain=request.get_host()).values_list(_C,flat=_Y)
	if siteID.count()==0:siteID=0
	else:siteID=siteID[0]
	return siteID
def get_comment(siteID,newsID,context):
	komentar=comment.objects.filter(site_id=siteID,post_id=newsID,active=_Y).order_by(_D).values(_S,_i,_A)
	for i in komentar:i[_A]=get_natural_datetime(i[_A])
	return komentar
def get_search_result(context,pdata):
	msplit=pdata.split('-');kriteria=[]
	for i in msplit:kriteria.append('Q(isi_berita__icontains="'+i+'")')
	all_kriteria=' & '.join(kriteria);res=berita.objects.filter(eval(all_kriteria)).order_by(_D)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def get_tags_result(context,pdata):
	pdata=re.sub('-',' ',pdata);res=berita.objects.filter(tags__nama=pdata).order_by(_D)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def document_clean(pdoc):document_test=pdoc;p=re.compile('<.*?>');document_test=p.sub('',document_test);document_test=re.sub('[^\\x00-\\x7F]+',' ',document_test);document_test=re.sub('@\\w+','',document_test);document_test=re.sub('\\s{2,}',' ',document_test);document_test=re.sub('&#;',"'",document_test);return document_test
def get_banner_all(siteID,context):banner=banner_all.objects.filter(site__id=siteID,status=Status.PUBLISHED);context['banner_all']=banner
def get_topSection(siteID,context,active_menu):
	namaOPD=Site.objects.filter(id=siteID).values_list(_S,flat=_Y)
	if namaOPD.count()>0:context['namaOPD']=namaOPD[0]
	mObjMenu=menus.ClsMenus();myMenu=menus.ClsMenus(siteID,_p);context[_j]=myMenu.get_menus();context['activeMenuList']=myMenu.find_activeMenuList(active_menu);context['socialMedia']=social_media.objects.filter(site_id=siteID);logoTop=logo.objects.filter(site_id=siteID,position=logo.Position.TOP)
	if logoTop.count()>0:context['logoTop']=logoTop[0].photo
	bannerTop=banner.objects.filter(site_id=siteID,position=banner.Position.TOP)
	if bannerTop.count()>0:context['bannerTop']=bannerTop[0]
def get_bottomSection(siteID,context,optID):
	E='https://widget.kominfo.go.id/data/covid-19/gpr.xml';D='get from server Widget';C='get from server (RSS)';B='https://kominfo.go.id/content/rss/laporan_isu_hoaks';A='feed';logoBottom=logo.objects.filter(site_id=siteID,position=logo.Position.BOTTOM)
	if logoBottom.count()>0:context['logoBottom']=logoBottom[0].photo
	context['instansi']=instansi.objects.filter(site_id=siteID)[:1]
	if optID==1:context['agenda']=agenda.objects.filter(site_id=siteID).order_by(_D)[:5]
	context[A]=_B
	if cache_item[_X]is _B:
		try:context[A]=feedparser.parse(B);cache_item[_X]=context[A];cache_item[_g]=datetime.datetime.now();print(C)
		except:pass
	elif (datetime.datetime.now()-cache_item[_g]).seconds>36000:
		try:context[A]=feedparser.parse(B);cache_item[_X]=context[A];cache_item[_g]=datetime.datetime.now();print(C)
		except:pass
	else:context[A]=cache_item[_X];print('get from cached (RSS)')
	if optID==1:
		context[_F]=_B;skrg=datetime.datetime.now()
		if cache_item[_F]is _B:
			try:
				if not settings.DEBUG:print(D);context[_F]=feedparser.parse(E)
				else:context[_F]=''
				cache_item[_F]=context[_F];simpan=datetime.datetime.now();cache_item[_h]=simpan.hour*3600+simpan.minute*60+simpan.second
			except:pass
		elif skrg.hour*3600+skrg.minute*60+skrg.second-cache_item[_h]>36000:
			try:
				if not settings.DEBUG:print(D);context[_F]=feedparser.parse(E)
				else:context[_F]=''
				cache_item[_F]=context[_F];simpan=datetime.datetime.now();cache_item[_h]=simpan.hour*3600+simpan.minute*60+simpan.second
			except:pass
		else:print('get from cached Widget');context[_F]=cache_item[_F]
def get_middleSection(siteID,context,optID):
	bannerBottom=banner.objects.filter(site_id=siteID,position=banner.Position.BOTTOM)
	if bannerBottom.count()>0:context['bannerBottom']=bannerBottom[0]
	context['linkTerkait']=get_linkTerkait(siteID);get_galeryFoto(siteID,context,optID);get_galeryVideo(siteID,context,optID)
def get_sideBar(siteID,context,opt):
	if opt==1:context['pejabat']=pejabat.objects.filter(site__id=siteID).order_by('jabatan_index')[:4]
	if opt==1 or opt==3:
		bannerMiddle1=banner.objects.filter(site_id=siteID,position=banner.Position.MIDDLE1)
		if bannerMiddle1.count()>0:context['bannerMiddle1']=bannerMiddle1[0]
		bannerMiddle2=banner.objects.filter(site_id=siteID,position=banner.Position.MIDDLE2)
		if bannerMiddle2.count()>0:context['bannerMiddle2']=bannerMiddle2[0]
	if opt==1:context['widget']=page_widget.objects.filter(site__id=siteID).order_by(_D)[:2]
	context['tags']=tags.objects.filter(site__id=siteID).order_by(_Z)
	if opt!=1:get_beritaTerbaru(siteID,context,3);get_beritaTerpopuler(siteID,context,3);get_pengumuman(siteID,context,3);get_artikel(siteID,context,3)
def get_beritaTerbaru(siteID,context,opt):
	B='beritaTerbaruAll';A='site__domain'
	if opt==1:maxNews=6
	elif opt==2:maxNews=100
	else:maxNews=3
	model_criteria={_q:OuterRef(_r)};subQry=get_topFoto(model_criteria);BeritaTerbaruLain=_B;BeritaTerbaruAll=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_a,_G,_I,_b,_J,_A,A).order_by(_D).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:BeritaTerbaruLain=berita.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_H,_a,_G,_I,_b,_J,_A,A).order_by(_D).distinct().annotate(foto=subQry)[:maxNews]
	if BeritaTerbaruLain:BeritaTerbaruAll=BeritaTerbaruAll.union(BeritaTerbaruLain);context[B]=BeritaTerbaruAll;context['beritaTerbaruLain']=BeritaTerbaruLain
	else:context[B]=BeritaTerbaruAll
	if BeritaTerbaruLain:
		for i in BeritaTerbaruLain:i[_A]=get_natural_datetime(i[_A])
	for i in BeritaTerbaruAll:i[_A]=get_natural_datetime(i[_A])
	return BeritaTerbaruAll
def get_beritaTerpopuler(siteID,context,opt):
	A='beritaTerpopulerAll'
	if opt==1:maxNews=6
	elif opt==2:maxNews=100
	else:maxNews=3
	model_criteria={_q:OuterRef(_r)};subQry=get_topFoto(model_criteria);BeritaTerpopulerLain=_B;BeritaQry=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
	if BeritaCount==0:BeritaCutOff=0
	else:BeritaCutOff=BeritaQry.order_by(_D).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
	BeritaTerpopulerAll=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_H,_a,_G,_I,_b,_J,_A).order_by(_k).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:
		BeritaQry=berita.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
		if BeritaCount==0:BeritaCutOff=0
		else:BeritaCutOff=BeritaQry.order_by(_D).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
		BeritaTerpopulerLain=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_H,_a,_G,_I,_b,_J,_A).order_by(_k).distinct().annotate(foto=subQry)[:maxNews]
	if BeritaTerpopulerLain:BeritaTerpopulerAll=BeritaTerpopulerAll.union(BeritaTerpopulerLain);context[A]=BeritaTerpopulerAll;context['beritaTerpopulerLain']=BeritaTerpopulerLain
	else:context[A]=BeritaTerpopulerAll
	if BeritaTerpopulerLain:
		for i in BeritaTerpopulerLain:i[_A]=get_natural_datetime(i[_A])
	for i in BeritaTerpopulerAll:i[_A]=get_natural_datetime(i[_A])
	return BeritaTerpopulerAll
def get_pengumuman(siteID,context,opt):
	B='pengumumanAll';A='isi_pengumuman'
	if opt==1:maxPengumuman=6
	elif opt==2:maxPengumuman=100
	else:maxPengumuman=3
	model_criteria={'pengumuman__id':OuterRef('photo__pengumuman__id')};subQry=get_topFoto(model_criteria);PengumumanLain=_B;PengumumanAll=pengumuman.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_G,_I,A,_J,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxPengumuman]
	if opt==1:PengumumanLain=pengumuman.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_H,_G,_I,A,_J,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxPengumuman]
	if PengumumanLain:PengumumanAll=PengumumanAll.union(PengumumanLain);context[B]=PengumumanAll;context['pengumumanLain']=PengumumanLain
	else:context[B]=PengumumanAll
	if PengumumanLain:
		for i in PengumumanLain:i[_A]=get_natural_datetime(i[_A])
	for i in PengumumanAll:i[_A]=get_natural_datetime(i[_A])
	return PengumumanAll
def get_artikel(siteID,context,opd):
	B='artikelAll';A='isi_artikel'
	if opd==1:maxArtikel=6
	elif opd==2:maxArtikel=100
	else:maxArtikel=3
	model_criteria={'artikel__id':OuterRef('photo__artikel__id')};subQry=get_topFoto(model_criteria);ArtikelLain=_B;ArtikelAll=artikel.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_G,_I,A,_J,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxArtikel]
	if opd==1:ArtikelLain=artikel.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_H,_G,_I,A,_J,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxArtikel]
	if ArtikelLain:ArtikelAll=ArtikelAll.union(ArtikelLain);context[B]=ArtikelAll;context['artikelLain']=ArtikelLain
	else:context[B]=ArtikelAll
	if ArtikelLain:
		for i in ArtikelLain:i[_A]=get_natural_datetime(i[_A])
	for i in ArtikelAll:i[_A]=get_natural_datetime(i[_A])
	return ArtikelAll
def get_beritaKategori(siteID,context,opt,kategori_slug):
	model_criteria={_q:OuterRef(_r)};subQry=get_topFoto(model_criteria);kategoriID=kategori.objects.filter(slug=kategori_slug).first();BeritaKategori=_B
	if kategoriID:BeritaKategori=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED,kategori_id=kategoriID.id).values(_C,_H,_a,_G,_I,_b,_J,_A).order_by(_D).distinct().annotate(foto=subQry)
	return BeritaKategori
def get_hitCounter(request,obj,content_type):
	if content_type!='site':
		hit_count=HitCount.objects.get_for_object(obj);hit_count_response=HitCountMixin.hit_count(request,hit_count);content_type_id=ContentType.objects.filter(model=content_type).first()
		if content_type_id:
			hit_update=HitCount.objects.filter(object_pk=obj.id,content_type_id=content_type_id.id).values_list('hits',flat=_Y)
			if hit_update.count()>0:obj.view_count=hit_update[0];obj.save()
def get_trending(siteID,context):
	maxData=7;trendingQry=berita.objects.filter(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_D).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending=trendingQry.filter(id__gte=trendingCutOff).order_by(_k).values_list(_C,_G,_I)[:maxData];trendingQry=berita.objects.exclude(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_D).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending_else=trendingQry.filter(id__gte=trendingCutOff).order_by(_k).values_list(_C,_G,_I)[:maxData]
	if trending_else:
		maxData_else=maxData-trending.count()
		if maxData_else>0:trending=trending.union(trending_else)
	context['trending']=trending
def get_galeryFoto(siteID,context,opd):
	A='galeryFoto'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryFoto=galery_foto.objects.filter(site_id=siteID).values(_C,_H,_G,_I,_c,_J,_A,_T).order_by(_D)[:mMax]
	for i in galeryFoto:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureFoto']=galeryFoto[:1]
		if galeryFoto.count()<=1:context[A]=galeryFoto
		else:context[A]=galeryFoto[1:mMax-1]
	elif opd==2:return galeryFoto
def get_popup(siteID,context):context['popup']=popup.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_J,_A,'status',_T).order_by(_d)[:1]
def get_galeryVideo(siteID,context,opd):
	A='galeryVideo'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryVideo=galery_video.objects.filter(site_id=siteID).values(_C,_H,_G,_J,_A,'embed','embed_video').order_by(_D)[:mMax]
	for i in galeryVideo:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureVideo']=galeryVideo[:1]
		if galeryVideo.count()<=1:context[A]=galeryVideo
		else:context[A]=galeryVideo[1:mMax-1]
	elif opd==2:return galeryVideo
def get_linkTerkait(siteID):linkTerkait=link_terkait.objects.filter(site__id=siteID).order_by(_C);return linkTerkait
def get_galeryLayanan(siteID,context):foto=galery_layanan.objects.filter(site_id=siteID,status=Status.PUBLISHED).order_by(_D)[:5];context['galeryLayanan']=foto
def get_meta(request,obj,context,jenis):
	F='%s';E='news_desc';D='%s://%s/%s/%s';C='news_img_meta';B='news_url';A='news_img';print('jenis = ');print(jenis);context['site_name']='%s://%s'%(request.scheme,request.get_host())
	if jenis==_U:
		context[A]=berita.photo.through.objects.filter(berita__id=obj.id).values(_T);print("context['news_img'] = ");print(context[A]);context['news_tags']=berita.tags.through.objects.filter(berita__id=obj.id).values('tags__nama');a=berita.objects.filter(id=obj.id)
		for i in a:print('schema = ',urlsplit(request.build_absolute_uri(_B)).scheme);print('schema2 = ',request.is_secure()and'https'or'http');context[B]=D%(request.scheme,request.get_host(),_U,i.judul_seo);context[E]=Truncator(strip_tags(i.isi_berita)).chars(160).strip();print("context['news_url'] = ");print(context[B])
		news_img_meta=berita.photo.through.objects.filter(berita__id=obj.id).order_by('photo__jenis')
		if news_img_meta.count()>0:context[C]='%s://%s%s'%(request.scheme,request.get_host(),news_img_meta[0].photo);print("context['news_img_meta'] = ");print(context[C])
	elif jenis==_e:
		context[A]=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id).values(_T);a=pengumuman.objects.filter(id=obj.id)
		for i in a:context[B]=D%(request.scheme,request.get_host(),_e,i.judul_seo);context[E]=SafeString(Truncator(i.isi_pengumuman).chars(160))
		news_img_meta=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[C]=F%news_img_meta[0].photo
	elif jenis==_f:
		context[A]=artikel.photo.through.objects.filter(artikel__id=obj.id).values(_T);a=artikel.objects.filter(id=obj.id)
		for i in a:context[B]=D%(request.scheme,request.get_host(),_f,i.judul_seo);context[E]=SafeString(Truncator(i.isi_artikel).chars(160))
		news_img_meta=artikel.photo.through.objects.filter(artikel__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[C]=F%news_img_meta[0].photo
	elif jenis==_j:
		context[A]=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id).values(_T);a=halaman_statis.objects.filter(id=obj.id)
		for i in a:context[B]=D%(request.scheme,request.get_host(),_j,i.judul);context[E]=SafeString(Truncator(i.isi_halaman).chars(160))
		news_img_meta=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[C]=F%news_img_meta[0].photo
def get_newsList(request,siteID,context,opt,section,jenis):
	news_per_page=6;mList=_B
	if section==_U:
		if jenis=='terbaru':mList=get_beritaTerbaru(siteID,context,opt)
		else:mList=get_beritaTerpopuler(siteID,context,opt)
	elif section==_e:mList=get_pengumuman(siteID,context,opt)
	elif section==_f:mList=get_artikel(siteID,context,opt)
	elif section=='kategori':mList=get_beritaKategori(siteID,context,opt,jenis)
	elif section=='galeri':
		if jenis=='video':mList=get_galeryVideo(siteID,context,opt)
		else:mList=get_galeryFoto(siteID,context,opt)
	elif section=='link':mList=get_linkTerkait(siteID)
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _B:page_number=1
		if page_number:context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
def get_statistik(request,siteID,context):
	tgl=datetime.datetime.now();Domain=request.get_host();hit_today=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day).count()
	if hit_today==0:hit_today=1
	context['hit_today']=hit_today;start_date=tgl+datetime.timedelta(days=-1);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_yesterday']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_this_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.date(end_date.year,end_date.month,end_date.day);context['hit_last_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();context['hit_this_month']=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month).count();start_date=add_months(tgl,-1);context['hit_last_month']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month).count();start_date=tgl+datetime.timedelta(hours=-1);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour);end_date=tgl;end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,end_date.hour);hit_online=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count()
	if hit_online==0:hit_online=1
	context['hit_online']=hit_online;context['hit_all']=Hit.objects.filter(domain=Domain).count()
def index(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	context[_O]='index';active_menu='beranda';optID=1
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_middleSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_trending(siteID,context);get_banner_all(siteID,context);get_beritaTerbaru(siteID,context,optID);get_pengumuman(siteID,context,optID);get_beritaTerpopuler(siteID,context,optID);get_artikel(siteID,context,optID);get_galeryLayanan(siteID,context);obj=Site.objects.get(id=siteID);get_hitCounter(request,obj,'site');get_statistik(request,siteID,context);get_popup(siteID,context);response=render(request,'opd/index.html',context);response.set_cookie(key=_S,value='my_value',samesite='None',secure=_Y);return response
def detail(request,pid,jenis):
	A='email';context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	if jenis==_U:
		news=get_object_or_404(berita,judul_seo=pid);get_hitCounter(request,news,_U);mList=get_comment(siteID,news.id,context);news_per_page=3
		if mList is not _B:
			paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
			if page_number is _B:page_number=1
			context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
		new_comment=_B
		if request.method==_R:
			comment_form=CommentForm(data=request.POST)
			if comment_form.is_valid():new_comment,created=comment.objects.get_or_create(site_id=siteID,name__iexact=request.POST.get(_S).strip(),body__iexact=request.POST.get(_i).strip(),defaults={'post':news,_i:request.POST.get(_i),_S:request.POST.get(_S),A:request.POST.get(A)})
		else:comment_form=CommentForm()
		context['new_comment']=new_comment;context['comment_form']=comment_form
	elif jenis==_e:news=get_object_or_404(pengumuman,judul_seo=pid);get_hitCounter(request,news,_e)
	elif jenis==_f:news=get_object_or_404(artikel,judul_seo=pid);get_hitCounter(request,news,_f)
	else:context[_K]='Halaman <b>%s</b> tidak ditemukan!'%pid;return render(request,_L,context)
	if news:news.created_at=get_natural_datetime(news.created_at)
	optID=3;context[_O]=jenis;context['news']=news;get_topSection(siteID,context,jenis);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);get_statistik(request,siteID,context);return render(request,_s,context)
def detail_list(request,section,jenis):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	optID=2;context[_O]=jenis;context['section']=section;active_menu=jenis
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_newsList(request,siteID,context,optID,section,jenis);get_statistik(request,siteID,context);return render(request,'opd/detail-list.html',context)
def search_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	optID=2;context[_O]=_E;active_menu=_E
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_statistik(request,siteID,context);context[_E]=pdata;mList=get_search_result(context,pdata);news_per_page=5
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _B:page_number=1
		context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
	return render(request,_t,context)
def tags_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	optID=2;context[_O]=_E;active_menu=_E
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_statistik(request,siteID,context);context[_E]=pdata;mList=get_tags_result(context,pdata);news_per_page=5
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _B:page_number=1
		context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
	return render(request,_t,context)
def halaman_statis_akses(request,slug):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	menu_id=menu.objects.filter(href='menu/'+slug);mFoundID=0;mNama=''
	for i in menu_id:
		mFoundID=i.id;mNama=i.nama
		if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID,is_edited=1).order_by(_d).exists():mFoundID=i.id;mNama=i.nama;break
	if mFoundID==0:
		for i in menu_id:
			if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID).order_by(_d).exists():mFoundID=i.id;mNama=i.nama;break
	news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_d)[:1];print('news [GET]= ');print(news)
	if not news:news=halaman_statis.objects.create(menu_id=mFoundID,site_id=siteID,judul=mNama,isi_halaman='Informasi tentang "'+mNama+'". Silahkan update di halaman <a target="_blank" href="/dashboard/halaman-statis/">Dashboard.<a>'+'<br><br><br><br>'+'"Halaman ini dibuat otomatis oleh sistem, karena halaman statis untuk menu ini belum dibuat. '+'<br>Silahkan lakukan update di halaman statis."',admin_id=request.user.id);news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_d)[:1];print('news [CREATE]= ');print(news)
	news=news.get();optID=3;jenis=_j;get_hitCounter(request,news,'halaman_statis');get_topSection(siteID,context,_U);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);get_statistik(request,siteID,context)
	if news:news.created_at=get_natural_datetime(news.created_at)
	context[_O]=jenis;context['news']=news;return render(request,_s,context)
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def dokumen_ajax(request,idx):
	A='file_path';max=5;siteID=get_siteID(request)
	if idx==0:
		object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_Z,_c,_P,A,_Q).order_by(_D)[:max];n=object_list.count()
		if max-n>0:object_list.union(dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_Z,_c,_P,A,_Q).order_by(_D)[:max-n])
	elif idx==1:object_list=dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_Z,_c,_P,A,_Q).order_by(_D)[:max]
	elif idx==2:object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_Z,_c,_P,A,_Q).order_by(_D)
	if idx==0 or idx==1 or idx==2:
		for i in object_list:i[_Q]=get_natural_datetime(i[_Q]);i[_P]=naturalsize(i[_P]);i[A]=settings.MEDIA_URL+i[A]
		mData=list(object_list)
	else:mData=_B
	return JsonResponse(mData,safe=_p)
def satudata_ajax(request,idx):
	if idx==0 or idx==1:
		for i in object_list:i[_Q]=get_natural_datetime(i[_Q]);i[_P]=naturalsize(i[_P])
		mData=list(object_list)
	else:mData=_B
	return JsonResponse(mData,safe=_p)
def satudata_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	optID=2;context[_O]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_statistik(request,siteID,context);return render(request,'opd/satudata-result.html',context)
def dokumen_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_N);return render(request,_L,context)
	optID=2;context[_O]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_statistik(request,siteID,context);return render(request,'opd/dokumen-result.html',context)