_s="template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_r='template'
_q='-updated_at'
_p='-created_at'
_o='num_pages'
_n='jumlah'
_m='page_obj'
_l='page'
_k='artikel'
_j='pengumuman'
_i='-view_count'
_h='body'
_g='berita'
_f='judul_seo'
_e='isi_berita'
_d='kategori__nama'
_c='photo__berita__id'
_b='berita__id'
_a='nama'
_Z=False
_Y='?page=1'
_X='/search/'
_W='photo__file_path'
_V='menu'
_U='name'
_T='POST'
_S='slug'
_R='updated_at'
_Q='size'
_P='jenis'
_O="Domain <b>%s</b> belum terdaftar, silahkan hubungi <br><a href='%s'>admin</a><br> untuk melakukan pendaftaran"
_N='account/error404.html'
_M='msg'
_L='\\s+'
_K='/admin'
_J=True
_I='admin__username'
_H='site__name'
_G=' '
_F='judul'
_E='search'
_D=None
_C='id'
_B='-id'
_A='created_at'
import calendar,datetime,re,feedparser
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import OuterRef,Q
from django.http import JsonResponse,Http404
from django.shortcuts import get_object_or_404,redirect,render
from django.utils.html import strip_tags
from django.utils.safestring import SafeString
from django.utils.text import Truncator,slugify
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from humanize import naturalsize
from account.commonf import get_topFoto
from django_opd.commonf import get_natural_datetime
from.models import comment,OptModelKinds,Log,AutoLatestNews
from hitcount.views import HitCountDetailView
from django.views.generic import TemplateView
from.import menus
from.forms import CommentForm
from.models import*
from easy_thumbnails.files import get_thumbnailer
from.hit_summary import do_summary
from hitcount.models import Hit
cache_item=dict()
cache_item['feed1']=_D
cache_item['date1']=_D
cache_item['feed2']=_D
cache_item['date2']=_D
def get_siteID(request):
	if request:siteID=Site.objects.filter(domain=request.get_host()).values_list(_C,flat=_J);return siteID[0]if siteID else 0
	return 0
def get_comment(siteID,newsID,context):
	komentar=comment.objects.filter(site_id=siteID,post_id=newsID,active=_J).order_by(_B).values(_U,_h,_A)
	for i in komentar:i[_A]=get_natural_datetime(i[_A])
	return komentar
def get_search_result(context,pdata):
	msplit=pdata.split('-');kriteria=[]
	for i in msplit:kriteria.append('Q(isi_berita__icontains="'+i+'")')
	all_kriteria=' & '.join(kriteria);res=berita.objects.filter(eval(all_kriteria)).order_by(_B)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def get_tags_result(context,pdata):
	pdata=re.sub('-',_G,pdata);res=berita.objects.filter(tags__nama=pdata).order_by(_B)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def document_clean(pdoc):document_test=pdoc;p=re.compile('<.*?>');document_test=p.sub('',document_test);document_test=re.sub('[^\\x00-\\x7F]+',_G,document_test);document_test=re.sub('@\\w+','',document_test);document_test=re.sub('\\s{2,}',_G,document_test);document_test=re.sub('&#;',"'",document_test);return document_test
def get_banner_all(siteID,context):banner=banner_all.objects.filter(site__id=siteID,status=Status.PUBLISHED).order_by(_B);context['banner_all']=banner
def get_weather(context):
	B='Weather:';A='weather';time_zone=getattr(settings,'TIME_ZONE','UTC');date_object=datetime.datetime.now(pytz.timezone(time_zone));a=Weather.objects.filter(tgl__lte=date_object).order_by('-tgl')[:1]
	if a:context[A]=a[0];print(B,a[0],a[0].tgl,a[0].weather_info)
	else:
		a=Weather.objects.filter(tgl__gte=date_object).order_by('tgl')[:1]
		if a:context[A]=a[0];print(B,a[0],a[0].tgl,a[0].weather_info)
def get_topSection(siteID,context,active_menu):
	namaOPD=Site.objects.filter(id=siteID).values_list(_U,flat=_J)
	if namaOPD.count()>0:context['namaOPD']=namaOPD[0]
	mObjMenu=menus.ClsMenus();myMenu=menus.ClsMenus(siteID,_Z);context[_V]=myMenu.get_menus();context['activeMenuList']=myMenu.find_activeMenuList(active_menu);context['socialMedia']=social_media.objects.filter(site_id=siteID);logoTop=logo.objects.filter(site_id=siteID,position=logo.Position.TOP)
	if logoTop.count()>0:context['logoTop']=logoTop[0].photo
	bannerTop=banner.objects.filter(site_id=siteID,position=banner.Position.TOP)
	if bannerTop.count()>0:context['bannerTop']=bannerTop[0]
def get_bottomSection(siteID,context,optID):
	A='-publish_date_convert';logoBottom=logo.objects.filter(site_id=siteID,position=logo.Position.BOTTOM)
	if logoBottom.count()>0:context['logoBottom']=logoBottom[0].photo
	context['instansi']=instansi.objects.filter(site_id=siteID)[:1]
	if optID==1:context['agenda']=agenda.objects.filter(site_id=siteID).order_by(_B)[:5]
	context['feed']=info_hoax.objects.order_by(A,_B)[:6]
	if optID==1:context['feed2']=info_widget.objects.order_by(A,_B)[:10]
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
	if opt==1:context['widget']=page_widget.objects.filter(site__id=siteID).order_by(_B)[:2]
	context['tags']=tags.objects.filter(site__id=siteID).order_by(_a)
	if opt!=1:get_beritaTerbaru(siteID,context,3);get_pengumuman(siteID,context,3);get_artikel(siteID,context,3)
def get_beritaTerbaru(siteID,context,opt):
	B='beritaTerbaruAll';A='site__domain'
	if opt==1:maxNews=6
	elif opt==2:maxNews=100
	else:maxNews=3
	model_criteria={_b:OuterRef(_c)};subQry=get_topFoto(model_criteria);BeritaTerbaruLain=_D;BeritaTerbaruAll=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_d,_F,_S,_e,_I,_A,A).order_by(_B).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:BeritaTerbaruLain=berita.objects.filter(status=Status.PUBLISHED).exclude(site_id=siteID).values(_C,_H,_d,_F,_S,_e,_I,_A,A).order_by(_B).distinct().annotate(foto=subQry)[:maxNews]
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
	model_criteria={_b:OuterRef(_c)};subQry=get_topFoto(model_criteria);BeritaTerpopulerLain=_D;BeritaQry=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
	if BeritaCount==0:BeritaCutOff=0
	else:BeritaCutOff=BeritaQry.order_by(_B).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
	BeritaTerpopulerAll=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_H,_d,_F,_S,_e,_I,_A).order_by(_i).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:
		BeritaQry=berita.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
		if BeritaCount==0:BeritaCutOff=0
		else:BeritaCutOff=BeritaQry.order_by(_B).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
		BeritaTerpopulerLain=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_H,_d,_F,_S,_e,_I,_A).order_by(_i).distinct().annotate(foto=subQry)[:maxNews]
	if BeritaTerpopulerLain:BeritaTerpopulerAll=BeritaTerpopulerAll.union(BeritaTerpopulerLain);context[A]=BeritaTerpopulerAll;context['beritaTerpopulerLain']=BeritaTerpopulerLain
	else:context[A]=BeritaTerpopulerAll
	if BeritaTerpopulerLain:
		for i in BeritaTerpopulerLain:i[_A]=get_natural_datetime(i[_A])
	for i in BeritaTerpopulerAll:i[_A]=get_natural_datetime(i[_A])
	return BeritaTerpopulerAll
def get_pengumuman(siteID,context,opt):
	A='isi_pengumuman'
	if opt==1:maxPengumuman=6
	elif opt==2:maxPengumuman=100
	else:maxPengumuman=3
	model_criteria={'pengumuman__id':OuterRef('photo__pengumuman__id')};subQry=get_topFoto(model_criteria);PengumumanLain=_D;PengumumanAll=pengumuman.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_F,_f,A,_I,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxPengumuman]
	if opt==1 and PengumumanAll:PengumumanLain=pengumuman.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_H,_F,_f,A,_I,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxPengumuman]
	context['pengumumanAll']=PengumumanAll;context['pengumumanLain']=PengumumanLain
	if PengumumanLain:
		for i in PengumumanLain:i[_A]=get_natural_datetime(i[_A])
	for i in PengumumanAll:i[_A]=get_natural_datetime(i[_A])
	return PengumumanAll
def get_artikel(siteID,context,opd):
	A='isi_artikel'
	if opd==1:maxArtikel=6
	elif opd==2:maxArtikel=100
	else:maxArtikel=3
	model_criteria={'artikel__id':OuterRef('photo__artikel__id')};subQry=get_topFoto(model_criteria);ArtikelLain=_D;ArtikelAll=artikel.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_F,_f,A,_I,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxArtikel]
	if opd==1 and ArtikelAll:ArtikelLain=artikel.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_H,_F,_f,A,_I,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxArtikel]
	context['artikelAll']=ArtikelAll;context['artikelLain']=ArtikelLain
	if ArtikelLain:
		for i in ArtikelLain:i[_A]=get_natural_datetime(i[_A])
	for i in ArtikelAll:i[_A]=get_natural_datetime(i[_A])
	return ArtikelAll
def get_beritaKategori(siteID,context,opt,kategori_slug):
	model_criteria={_b:OuterRef(_c)};subQry=get_topFoto(model_criteria);kategoriID=kategori.objects.filter(slug=kategori_slug).first();BeritaKategori=_D
	if kategoriID:BeritaKategori=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED,kategori_id=kategoriID.id).values(_C,_H,_d,_F,_S,_e,_I,_A).order_by(_B).distinct().annotate(foto=subQry)
	return BeritaKategori
def get_hitCounter(request,obj,content_type):
	hit_count=HitCount.objects.get_for_object(obj);hit_count_response=HitCountMixin.hit_count(request,hit_count);content_type_id=ContentType.objects.filter(model=content_type).first()
	if content_type_id:
		hit_update=HitCount.objects.filter(object_pk=obj.id,content_type_id=content_type_id.id).values_list('hits',flat=_J)
		if hit_update.count()>0:obj.view_count=hit_update[0];obj.save()
def get_trending(siteID,context):
	maxData=7;trendingQry=berita.objects.filter(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_B).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending=trendingQry.filter(id__gte=trendingCutOff).order_by(_i).values_list(_C,_F,_S)[:maxData];trendingQry=berita.objects.exclude(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_B).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending_else=trendingQry.filter(id__gte=trendingCutOff).order_by(_i).values_list(_C,_F,_S)[:maxData]
	if trending_else:
		maxData_else=maxData-trending.count()
		if maxData_else>0:trending=trending.union(trending_else)
	context['trending']=trending
def get_galeryFoto(siteID,context,opd):
	A='galeryFoto'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryFoto=galery_foto.objects.filter(site_id=siteID).values(_C,_H,_F,_f,_I,_A,_W).order_by(_B)[:mMax]
	for i in galeryFoto:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureFoto']=galeryFoto[:1]
		if galeryFoto.count()<=1:context[A]=galeryFoto
		else:context[A]=galeryFoto[1:mMax-1]
	elif opd==2:return galeryFoto
def get_popup(siteID,context):context['popup']=popup.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_H,_I,_A,'status',_W).order_by(_q)[:1]
def get_galeryVideo(siteID,context,opd):
	A='galeryVideo'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryVideo=galery_video.objects.filter(site_id=siteID).values(_C,_H,_F,_I,_A,'embed','embed_video').order_by(_B)[:mMax]
	for i in galeryVideo:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureVideo']=galeryVideo[:1]
		if galeryVideo.count()<=1:context[A]=galeryVideo
		else:context[A]=galeryVideo[1:mMax-1]
	elif opd==2:return galeryVideo
def get_linkTerkait(siteID):linkTerkait=link_terkait.objects.filter(site__id=siteID).order_by(_C);return linkTerkait
def get_galeryLayanan(siteID,context):foto=galery_layanan.objects.filter(site_id=siteID,status=Status.PUBLISHED).order_by(_B)[:5];context['galeryLayanan']=foto
def get_meta(request,obj,context,jenis):
	I='is_mobile';H='%s://%s%s';G='news_img_meta';F='news_title';E='news_desc';D='%s://%s/%s/%s/';C='news_url';B='news_img';A='https';context['site_name']='%s://%s'%(A,request.get_host());context['news_type']=jenis if jenis!=_V else'pages';context[I]=request.device[I]
	if jenis==_g:
		context[B]=berita.photo.through.objects.filter(berita__id=obj.id).values(_W);print("context['news_img'] = ");print(context[B]);context['news_tags']=berita.tags.through.objects.filter(berita__id=obj.id).values('tags__nama');model_criteria={_b:OuterRef(_c)};subQry=get_topFoto(model_criteria);a=berita.objects.filter(id=obj.id).annotate(foto=subQry)[:1]
		for i in a:context[C]=D%(A,request.get_host(),_g,i.slug);tmp=Truncator(strip_tags(i.isi_berita)).words(30);context[E]=re.sub(_L,_G,tmp);tmp=strip_tags(i.judul);context[F]=re.sub(_L,_G,tmp);context[G]=i.foto;print('type FOTO',type(i.foto))
	elif jenis==_j:
		context[B]=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id).values(_W);a=pengumuman.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_j,i.judul_seo);tmp=Truncator(strip_tags(i.isi_pengumuman)).words(30);context[E]=re.sub(_L,_G,tmp);tmp=strip_tags(i.judul);context[F]=re.sub(_L,_G,tmp)
		news_img_meta=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
	elif jenis==_k:
		context[B]=artikel.photo.through.objects.filter(artikel__id=obj.id).values(_W);a=artikel.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_k,i.judul_seo);tmp=Truncator(strip_tags(i.isi_artikel)).words(30);context[E]=re.sub(_L,_G,tmp);tmp=strip_tags(i.judul);context[F]=re.sub(_L,_G,tmp)
		news_img_meta=artikel.photo.through.objects.filter(artikel__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
	elif jenis==_V:
		context[B]=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id).values(_W);a=halaman_statis.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_V,i.judul);tmp=Truncator(strip_tags(i.isi_halaman)).words(30);context[E]=re.sub(_L,_G,tmp);tmp=strip_tags(i.judul);context[F]=re.sub(_L,_G,tmp)
		news_img_meta=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
def get_newsList(request,siteID,context,opt,section,jenis):
	news_per_page=6;mList=_D
	if section==_g:
		if jenis=='terbaru':mList=get_beritaTerbaru(siteID,context,opt)
		else:mList=get_beritaTerpopuler(siteID,context,opt)
	elif section==_j:mList=get_pengumuman(siteID,context,opt)
	elif section==_k:mList=get_artikel(siteID,context,opt)
	elif section=='kategori':mList=get_beritaKategori(siteID,context,opt,jenis)
	elif section=='galeri':
		if jenis=='video':mList=get_galeryVideo(siteID,context,opt)
		else:mList=get_galeryFoto(siteID,context,opt)
	elif section=='link':mList=get_linkTerkait(siteID)
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _D:page_number=1
		if page_number:context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
def get_statistik(request,siteID,context):
	tgl=datetime.datetime.now();Domain=request.get_host();hit_today=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day).count()
	if hit_today==0:hit_today=1
	context['hit_today']=hit_today;start_date=tgl+datetime.timedelta(days=-1);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_yesterday']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_this_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.date(end_date.year,end_date.month,end_date.day);context['hit_last_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();context['hit_this_month']=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month).count();start_date=add_months(tgl,-1);context['hit_last_month']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month).count();start_date=tgl+datetime.timedelta(hours=-1);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour);end_date=tgl;end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,end_date.hour);hit_online=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count()
	if hit_online==0:hit_online=1
	context['hit_online']=hit_online;context['hit_all']=Hit.objects.filter(domain=Domain).count()
def index(request):
	context={};siteID=get_siteID(request)
	if not siteID:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	context[_P]='index';active_menu='beranda';optID=1
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_middleSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_trending(siteID,context);get_banner_all(siteID,context);get_beritaTerbaru(siteID,context,optID);context['autolatestnews']=get_autolatestnews(siteID);get_pengumuman(siteID,context,optID);get_artikel(siteID,context,optID);get_galeryLayanan(siteID,context);get_popup(siteID,context);get_weather(context);template_name=get_template(siteID);print('TEMPLATENAME',template_name);response=render(request,f"{template_name}index.html",context);response.set_cookie(key=_U,value='my_value',samesite='None',secure=_J);return response
def detail(request,pid,jenis):
	A='email';context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	if jenis==_g:
		news=get_object_or_404(berita,slug=pid);mList=get_comment(siteID,news.id,context);news_per_page=3
		if mList is not _D:
			paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
			if page_number is _D:page_number=1
			context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
		new_comment=_D
		if request.method==_T:
			comment_form=CommentForm(data=request.POST)
			if comment_form.is_valid():new_comment,created=comment.objects.get_or_create(site_id=siteID,name__iexact=request.POST.get(_U).strip(),body__iexact=request.POST.get(_h).strip(),defaults={'post':news,_h:request.POST.get(_h),_U:request.POST.get(_U),A:request.POST.get(A)})
		else:comment_form=CommentForm()
		context['new_comment']=new_comment;context['comment_form']=comment_form
	elif jenis==_j:news=get_object_or_404(pengumuman,judul_seo=pid)
	elif jenis==_k:news=get_object_or_404(artikel,judul_seo=pid)
	else:context[_M]='Halaman <b>%s</b> tidak ditemukan!'%pid;return render(request,_N,context)
	if news:news.created_at=get_natural_datetime(news.created_at)
	optID=3;context[_P]=jenis;context['news']=news;get_topSection(siteID,context,jenis);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);template_name=get_template(siteID);return render(request,f"{template_name}detail.html",context)
def detail_list(request,section,jenis):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	optID=2;context[_P]=jenis;context['section']=section;active_menu=jenis
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_newsList(request,siteID,context,optID,section,jenis);template_name=get_template(siteID);return render(request,f"{template_name}detail-list.html",context)
def search_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	optID=2;context[_P]=_E;active_menu=_E
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);context[_E]=pdata;mList=get_search_result(context,pdata);news_per_page=5
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _D:page_number=1
		context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
	template_name=get_template(siteID);return render(request,f"{template_name}search-result.html",context)
def tags_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	optID=2;context[_P]=_E;active_menu=_E
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);context[_E]=pdata;mList=get_tags_result(context,pdata);news_per_page=5
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_l)
		if page_number is _D:page_number=1
		context[_m]=paginator.get_page(page_number);context[_n]=paginator.page_range;context[_o]=paginator.num_pages
	template_name=get_template(siteID);return render(request,f"{template_name}/search-result.html",context)
def halaman_statis_akses(request,slug):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	if request.method==_T:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_X+slugify(pdata)+_Y)
	print('slug=',slug);menu_id=menu.objects.filter(href='menu/'+slug);print('count = ',menu_id.count())
	for i in menu_id:print(_V,i.id,i.nama)
	mFoundID=0;mNama=''
	for i in menu_id:
		mFoundID=i.id;mNama=i.nama
		if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID,is_edited=1).order_by(_p).exists():mFoundID=i.id;mNama=i.nama;break
	if mFoundID==0:
		for i in menu_id:
			if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID).order_by(_p).exists():mFoundID=i.id;mNama=i.nama;break
	news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_q)[:1]
	if not news:news=halaman_statis.objects.create(menu_id=mFoundID,site_id=siteID,judul=mNama,isi_halaman='Informasi tentang "'+mNama+'". Silahkan update di halaman <a target="_blank" href="/dashboard/halaman-statis/">Dashboard.<a>'+'<br><br><br><br>'+'"Halaman ini dibuat otomatis oleh sistem, karena halaman statis untuk menu ini belum dibuat. '+'<br>Silahkan lakukan update di halaman statis."',admin_id=request.user.id);news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_q)[:1]
	news=news.get();optID=3;jenis=_V;get_topSection(siteID,context,_g);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis)
	if news:news.created_at=get_natural_datetime(news.created_at)
	context[_P]=jenis;context['news']=news;template_name=get_template(siteID);return render(request,f"{template_name}detail.html",context)
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def dokumen_ajax(request,idx):
	B='deskripsi';A='file_path';max=5;siteID=get_siteID(request)
	if idx==0:
		object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_Q,A,_R).order_by(_B)[:max];n=object_list.count()
		if max-n>0:object_list.union(dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_Q,A,_R).order_by(_B)[:max-n])
	elif idx==1:object_list=dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_Q,A,_R).order_by(_B)[:max]
	elif idx==2:object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_Q,A,_R).order_by(_B)
	if idx==0 or idx==1 or idx==2:
		for i in object_list:i[_R]=get_natural_datetime(i[_R]);i[_Q]=naturalsize(i[_Q]);i[A]=settings.MEDIA_URL+i[A]
		mData=list(object_list)
	else:mData=_D
	return JsonResponse(mData,safe=_Z)
def satudata_ajax(request,idx):
	if idx==0 or idx==1:
		for i in object_list:i[_R]=get_natural_datetime(i[_R]);i[_Q]=naturalsize(i[_Q])
		mData=list(object_list)
	else:mData=_D
	return JsonResponse(mData,safe=_Z)
def satudata_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	optID=2;context[_P]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);template_name=get_template(siteID);return render(request,f"{template_name}/satudata-result.html",context)
def dokumen_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_K);return render(request,_N,context)
	optID=2;context[_P]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);template_name=get_template(siteID);return render(request,f"{template_name}/dokumen-result.html",context)
def get_template_id(site_id,is_frontend=_J):
	print('site',site_id);template=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list(_C,flat=_J)[:1];print(_r,template)
	if template:return template[0]
	raise Http404(_s%_K)
def get_template(site_id,is_frontend=_J):
	print('site',site_id);template=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('rel_path',flat=_J)[:1];print(_r,template)
	if template:return template[0]
	raise Http404(_s%_K)
def check_need_refresh(site_id,kind,expired_in):
	initial_date=timezone.now();is_refresh=_Z;tmp_log=Log.objects.filter(site_id=site_id,kind=kind)
	if not tmp_log:is_refresh=_J;Log.objects.create(site_id=site_id,kind=kind,expired=initial_date+datetime.timedelta(days=expired_in))
	else:
		is_refresh=tmp_log[0].is_need_refresh;print('IS NEED TO REFRESH=',is_refresh)
		if is_refresh:post=tmp_log[0];post.is_need_refresh=_Z;post.expired=initial_date+datetime.timedelta(days=expired_in);post.save()
	if not is_refresh:
		if tmp_log:
			tmp_expired=tmp_log[0].expired;tmp_diff=(tmp_expired-initial_date).days;print('date diff',tmp_diff)
			if tmp_diff<0:is_refresh=_J;post=tmp_log[0];post.expired=initial_date+datetime.timedelta(days=expired_in);post.save()
	return is_refresh
def get_autolatestnews(site_id,max_data=15):
	kind=OptModelKinds.NEWS;most_view_within=30;expired_in=1
	if check_need_refresh(site_id,kind,expired_in):
		print('Refresh need to refresh');AutoLatestNews.objects.filter(site_id=site_id,kind=kind).delete();count_days=timezone.now()-datetime.timedelta(days=most_view_within);count_days=count_days.replace(hour=0,minute=0,second=0,microsecond=0);model_criteria={_b:OuterRef(_c)};subQry=get_topFoto(model_criteria);obj_news=berita.objects.filter(site_id=site_id,status=Status.PUBLISHED,created_at__gte=count_days).annotate(file_path=subQry).order_by(_p)[:max_data];mcount=obj_news.count();print('mcount',mcount)
		if mcount<max_data:print('obj_news',obj_news);obj_news_add=berita.objects.filter(site_id=site_id,status=Status.PUBLISHED,updated_at__lt=count_days).annotate(file_path=subQry).order_by(_A)[:max_data-mcount];obj_news=obj_news.union(obj_news_add)
		for i in obj_news:sub_title=Truncator(strip_tags(i.isi_berita)).words(30);sub_title=re.sub(_L,_G,sub_title);obj=AutoLatestNews.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.judul,sub_title=sub_title,slug=i.slug,categories=i.kategori,kind=OptModelKinds.NEWS,created_at=i.created_at,photo_path=i.file_path)
	obj=AutoLatestNews.objects.filter(site_id=site_id,kind=kind).order_by(_p)[:max_data];print('obj autolatestnews',obj.count())
	for i in obj:i.created_at_str=get_natural_datetime(i.created_at)
	return obj