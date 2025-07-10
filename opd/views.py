_p="template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_o='template'
_n='-updated_at'
_m=False
_l='num_pages'
_k='jumlah'
_j='page_obj'
_i='page'
_h='artikel'
_g='pengumuman'
_f='-view_count'
_e='photo__berita__id'
_d='berita__id'
_c='body'
_b='berita'
_a='judul_seo'
_Z='isi_berita'
_Y='kategori__nama'
_X='nama'
_W='?page=1'
_V='/search/'
_U='photo__file_path'
_T='menu'
_S='name'
_R='POST'
_Q='slug'
_P='updated_at'
_O='size'
_N='jenis'
_M="Domain <b>%s</b> belum terdaftar, silahkan hubungi <br><a href='%s'>admin</a><br> untuk melakukan pendaftaran"
_L='account/error404.html'
_K='msg'
_J=True
_I='/admin'
_H='admin__username'
_G='site__name'
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
from opd.models import comment
from hitcount.views import HitCountDetailView
from django.views.generic import TemplateView
from .  import menus
from .forms import CommentForm
from .models import *
from easy_thumbnails.files import get_thumbnailer
from .hit_summary import do_summary
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
	komentar=comment.objects.filter(site_id=siteID,post_id=newsID,active=_J).order_by(_B).values(_S,_c,_A)
	for i in komentar:i[_A]=get_natural_datetime(i[_A])
	return komentar
def get_search_result(context,pdata):
	msplit=pdata.split('-');kriteria=[]
	for i in msplit:kriteria.append('Q(isi_berita__icontains="'+i+'")')
	all_kriteria=' & '.join(kriteria);res=berita.objects.filter(eval(all_kriteria)).order_by(_B)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def get_tags_result(context,pdata):
	pdata=re.sub('-',' ',pdata);res=berita.objects.filter(tags__nama=pdata).order_by(_B)
	for i in res:i.isi_berita=document_clean(i.isi_berita)
	return res
def document_clean(pdoc):document_test=pdoc;p=re.compile('<.*?>');document_test=p.sub('',document_test);document_test=re.sub('[^\\x00-\\x7F]+',' ',document_test);document_test=re.sub('@\\w+','',document_test);document_test=re.sub('\\s{2,}',' ',document_test);document_test=re.sub('&#;',"'",document_test);return document_test
def get_banner_all(siteID,context):banner=banner_all.objects.filter(site__id=siteID,status=Status.PUBLISHED).order_by(_B);context['banner_all']=banner
def get_weather(context):
	B='Weather:';A='weather';time_zone=getattr(settings,'TIME_ZONE','UTC');date_object=datetime.datetime.now(pytz.timezone(time_zone));a=Weather.objects.filter(tgl__lte=date_object).order_by('-tgl')[:1]
	if a:context[A]=a[0];
	else:
		a=Weather.objects.filter(tgl__gte=date_object).order_by('tgl')[:1]
		if a:context[A]=a[0];
def get_topSection(siteID,context,active_menu):
	namaOPD=Site.objects.filter(id=siteID).values_list(_S,flat=_J)
	if namaOPD.count()>0:context['namaOPD']=namaOPD[0]
	mObjMenu=menus.ClsMenus();myMenu=menus.ClsMenus(siteID,_m);context[_T]=myMenu.get_menus();context['activeMenuList']=myMenu.find_activeMenuList(active_menu);context['socialMedia']=social_media.objects.filter(site_id=siteID);logoTop=logo.objects.filter(site_id=siteID,position=logo.Position.TOP)
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
	context['tags']=tags.objects.filter(site__id=siteID).order_by(_X)
	if opt!=1:get_beritaTerbaru(siteID,context,3);get_pengumuman(siteID,context,3);get_artikel(siteID,context,3)
def get_beritaTerbaru(siteID,context,opt):
	B='beritaTerbaruAll';A='site__domain'
	if opt==1:maxNews=6
	elif opt==2:maxNews=100
	else:maxNews=3
	model_criteria={_d:OuterRef(_e)};subQry=get_topFoto(model_criteria);BeritaTerbaruLain=_D;BeritaTerbaruAll=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_G,_Y,_F,_Q,_Z,_H,_A,A).order_by(_B).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:BeritaTerbaruLain=berita.objects.filter(status=Status.PUBLISHED).exclude(site_id=siteID).values(_C,_G,_Y,_F,_Q,_Z,_H,_A,A).order_by(_B).distinct().annotate(foto=subQry)[:maxNews]
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
	model_criteria={_d:OuterRef(_e)};subQry=get_topFoto(model_criteria);BeritaTerpopulerLain=_D;BeritaQry=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
	if BeritaCount==0:BeritaCutOff=0
	else:BeritaCutOff=BeritaQry.order_by(_B).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
	BeritaTerpopulerAll=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_G,_Y,_F,_Q,_Z,_H,_A).order_by(_f).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:
		BeritaQry=berita.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
		if BeritaCount==0:BeritaCutOff=0
		else:BeritaCutOff=BeritaQry.order_by(_B).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
		BeritaTerpopulerLain=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_G,_Y,_F,_Q,_Z,_H,_A).order_by(_f).distinct().annotate(foto=subQry)[:maxNews]
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
	model_criteria={'pengumuman__id':OuterRef('photo__pengumuman__id')};subQry=get_topFoto(model_criteria);PengumumanLain=_D;PengumumanAll=pengumuman.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_G,_F,_a,A,_H,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxPengumuman]
	if opt==1 and PengumumanAll:PengumumanLain=pengumuman.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_G,_F,_a,A,_H,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxPengumuman]
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
	model_criteria={'artikel__id':OuterRef('photo__artikel__id')};subQry=get_topFoto(model_criteria);ArtikelLain=_D;ArtikelAll=artikel.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_G,_F,_a,A,_H,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxArtikel]
	if opd==1 and ArtikelAll:ArtikelLain=artikel.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_G,_F,_a,A,_H,_A).order_by(_B).distinct().annotate(foto=subQry)[:maxArtikel]
	context['artikelAll']=ArtikelAll;context['artikelLain']=ArtikelLain
	if ArtikelLain:
		for i in ArtikelLain:i[_A]=get_natural_datetime(i[_A])
	for i in ArtikelAll:i[_A]=get_natural_datetime(i[_A])
	return ArtikelAll
def get_beritaKategori(siteID,context,opt,kategori_slug):
	model_criteria={_d:OuterRef(_e)};subQry=get_topFoto(model_criteria);kategoriID=kategori.objects.filter(slug=kategori_slug).first();BeritaKategori=_D
	if kategoriID:BeritaKategori=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED,kategori_id=kategoriID.id).values(_C,_G,_Y,_F,_Q,_Z,_H,_A).order_by(_B).distinct().annotate(foto=subQry)
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
	trending=trendingQry.filter(id__gte=trendingCutOff).order_by(_f).values_list(_C,_F,_Q)[:maxData];trendingQry=berita.objects.exclude(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_B).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending_else=trendingQry.filter(id__gte=trendingCutOff).order_by(_f).values_list(_C,_F,_Q)[:maxData]
	if trending_else:
		maxData_else=maxData-trending.count()
		if maxData_else>0:trending=trending.union(trending_else)
	context['trending']=trending
def get_galeryFoto(siteID,context,opd):
	A='galeryFoto'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryFoto=galery_foto.objects.filter(site_id=siteID).values(_C,_G,_F,_a,_H,_A,_U).order_by(_B)[:mMax]
	for i in galeryFoto:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureFoto']=galeryFoto[:1]
		if galeryFoto.count()<=1:context[A]=galeryFoto
		else:context[A]=galeryFoto[1:mMax-1]
	elif opd==2:return galeryFoto
def get_popup(siteID,context):context['popup']=popup.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_G,_H,_A,'status',_U).order_by(_n)[:1]
def get_galeryVideo(siteID,context,opd):
	A='galeryVideo'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryVideo=galery_video.objects.filter(site_id=siteID).values(_C,_G,_F,_H,_A,'embed','embed_video').order_by(_B)[:mMax]
	for i in galeryVideo:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureVideo']=galeryVideo[:1]
		if galeryVideo.count()<=1:context[A]=galeryVideo
		else:context[A]=galeryVideo[1:mMax-1]
	elif opd==2:return galeryVideo
def get_linkTerkait(siteID):linkTerkait=link_terkait.objects.filter(site__id=siteID).order_by(_C);return linkTerkait
def get_galeryLayanan(siteID,context):foto=galery_layanan.objects.filter(site_id=siteID,status=Status.PUBLISHED).order_by(_B)[:5];context['galeryLayanan']=foto
def get_meta(request,obj,context,jenis):
	I='is_mobile';H='%s://%s%s';G='news_img_meta';F='news_title';E='news_desc';D='%s://%s/%s/%s/';C='news_url';B='news_img';A='https';context['site_name']='%s://%s'%(A,request.get_host());context['news_type']=jenis if jenis!=_T else'pages';context[I]=request.device[I]
	if jenis==_b:
		context[B]=berita.photo.through.objects.filter(berita__id=obj.id).values(_U);context['news_tags']=berita.tags.through.objects.filter(berita__id=obj.id).values('tags__nama');model_criteria={_d:OuterRef(_e)};subQry=get_topFoto(model_criteria);a=berita.objects.filter(id=obj.id).annotate(foto=subQry)[:1]
		for i in a:context[C]=D%(A,request.get_host(),_b,i.slug);context[E]=Truncator(strip_tags(i.isi_berita)).words(30).strip();context[F]=Truncator(strip_tags(i.judul)).strip();context[G]=i.foto
	elif jenis==_g:
		context[B]=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id).values(_U);a=pengumuman.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_g,i.judul_seo);context[E]=Truncator(strip_tags(i.isi_pengumuman)).words(30).strip();context[F]=Truncator(strip_tags(i.judul)).words(15).strip()
		news_img_meta=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
	elif jenis==_h:
		context[B]=artikel.photo.through.objects.filter(artikel__id=obj.id).values(_U);a=artikel.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_h,i.judul_seo);context[E]=Truncator(strip_tags(i.isi_artikel)).words(30).strip();context[F]=Truncator(strip_tags(i.judul)).words(15).strip()
		news_img_meta=artikel.photo.through.objects.filter(artikel__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
	elif jenis==_T:
		context[B]=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id).values(_U);a=halaman_statis.objects.filter(id=obj.id)
		for i in a:context[C]=D%(A,request.get_host(),_T,i.judul);context[E]=Truncator(strip_tags(i.isi_halaman)).words(30).strip();context[F]=Truncator(strip_tags(i.judul)).words(15).strip()
		news_img_meta=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[G]=H%(A,request.get_host(),news_img_meta[0].photo)
def get_newsList(request,siteID,context,opt,section,jenis):
	news_per_page=6;mList=_D
	if section==_b:
		if jenis=='terbaru':mList=get_beritaTerbaru(siteID,context,opt)
		else:mList=get_beritaTerpopuler(siteID,context,opt)
	elif section==_g:mList=get_pengumuman(siteID,context,opt)
	elif section==_h:mList=get_artikel(siteID,context,opt)
	elif section=='kategori':mList=get_beritaKategori(siteID,context,opt,jenis)
	elif section=='galeri':
		if jenis=='video':mList=get_galeryVideo(siteID,context,opt)
		else:mList=get_galeryFoto(siteID,context,opt)
	elif section=='link':mList=get_linkTerkait(siteID)
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_i)
		if page_number is _D:page_number=1
		if page_number:context[_j]=paginator.get_page(page_number);context[_k]=paginator.page_range;context[_l]=paginator.num_pages
def get_statistik(request,siteID,context):
	tgl=datetime.datetime.now();Domain=request.get_host();hit_today=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day).count()
	if hit_today==0:hit_today=1
	context['hit_today']=hit_today;start_date=tgl+datetime.timedelta(days=-1);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_yesterday']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-7);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=datetime.date(tgl.year,tgl.month,tgl.day);context['hit_this_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();start_date=tgl+datetime.timedelta(days=-14);start_date=datetime.date(start_date.year,start_date.month,start_date.day);end_date=tgl+datetime.timedelta(days=-7);end_date=datetime.date(end_date.year,end_date.month,end_date.day);context['hit_last_week']=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count();context['hit_this_month']=Hit.objects.filter(domain=Domain,created__year=tgl.year,created__month=tgl.month).count();start_date=add_months(tgl,-1);context['hit_last_month']=Hit.objects.filter(domain=Domain,created__year=start_date.year,created__month=start_date.month).count();start_date=tgl+datetime.timedelta(hours=-1);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour);end_date=tgl;end_date=datetime.datetime(end_date.year,end_date.month,end_date.day,end_date.hour);hit_online=Hit.objects.filter(domain=Domain,created__range=(start_date,end_date)).count()
	if hit_online==0:hit_online=1
	context['hit_online']=hit_online;context['hit_all']=Hit.objects.filter(domain=Domain).count()
def index(request):
	context={};siteID=get_siteID(request)
	if not siteID:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	context[_N]='index';active_menu='beranda';optID=1
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_middleSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_trending(siteID,context);get_banner_all(siteID,context);get_beritaTerbaru(siteID,context,optID);get_pengumuman(siteID,context,optID);get_artikel(siteID,context,optID);get_galeryLayanan(siteID,context);get_popup(siteID,context);get_weather(context);template_name=get_template(siteID);response=render(request,f"{template_name}index.html",context);response.set_cookie(key=_S,value='my_value',samesite='None',secure=_J);return response
def detail(request,pid,jenis):
	A='email';context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	if jenis==_b:
		news=get_object_or_404(berita,slug=pid);mList=get_comment(siteID,news.id,context);news_per_page=3
		if mList is not _D:
			paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_i)
			if page_number is _D:page_number=1
			context[_j]=paginator.get_page(page_number);context[_k]=paginator.page_range;context[_l]=paginator.num_pages
		new_comment=_D
		if request.method==_R:
			comment_form=CommentForm(data=request.POST)
			if comment_form.is_valid():new_comment,created=comment.objects.get_or_create(site_id=siteID,name__iexact=request.POST.get(_S).strip(),body__iexact=request.POST.get(_c).strip(),defaults={'post':news,_c:request.POST.get(_c),_S:request.POST.get(_S),A:request.POST.get(A)})
		else:comment_form=CommentForm()
		context['new_comment']=new_comment;context['comment_form']=comment_form
	elif jenis==_g:news=get_object_or_404(pengumuman,judul_seo=pid)
	elif jenis==_h:news=get_object_or_404(artikel,judul_seo=pid)
	else:context[_K]='Halaman <b>%s</b> tidak ditemukan!'%pid;return render(request,_L,context)
	if news:news.created_at=get_natural_datetime(news.created_at)
	optID=3;context[_N]=jenis;context['news']=news;get_topSection(siteID,context,jenis);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);template_name=get_template(siteID);return render(request,f"{template_name}detail.html",context)
def detail_list(request,section,jenis):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	optID=2;context[_N]=jenis;context['section']=section;active_menu=jenis
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_newsList(request,siteID,context,optID,section,jenis);template_name=get_template(siteID);return render(request,f"{template_name}detail-list.html",context)
def search_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	optID=2;context[_N]=_E;active_menu=_E
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);context[_E]=pdata;mList=get_search_result(context,pdata);news_per_page=5
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_i)
		if page_number is _D:page_number=1
		context[_j]=paginator.get_page(page_number);context[_k]=paginator.page_range;context[_l]=paginator.num_pages
	template_name=get_template(siteID);return render(request,f"{template_name}search-result.html",context)
def tags_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	optID=2;context[_N]=_E;active_menu=_E
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);context[_E]=pdata;mList=get_tags_result(context,pdata);news_per_page=5
	if mList is not _D:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_i)
		if page_number is _D:page_number=1
		context[_j]=paginator.get_page(page_number);context[_k]=paginator.page_range;context[_l]=paginator.num_pages
	template_name=get_template(siteID);return render(request,f"{template_name}/search-result.html",context)
def halaman_statis_akses(request,slug):
	A='-created_at';context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	if request.method==_R:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_V+slugify(pdata)+_W)
	menu_id=menu.objects.filter(href='menu/'+slug);
	for i in menu_id:pass
	mFoundID=0;mNama=''
	for i in menu_id:
		mFoundID=i.id;mNama=i.nama
		if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID,is_edited=1).order_by(A).exists():mFoundID=i.id;mNama=i.nama;break
	if mFoundID==0:
		for i in menu_id:
			if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID).order_by(A).exists():mFoundID=i.id;mNama=i.nama;break
	news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_n)[:1]
	if not news:news=halaman_statis.objects.create(menu_id=mFoundID,site_id=siteID,judul=mNama,isi_halaman='Informasi tentang "'+mNama+'". Silahkan update di halaman <a target="_blank" href="/dashboard/halaman-statis/">Dashboard.<a>'+'<br><br><br><br>'+'"Halaman ini dibuat otomatis oleh sistem, karena halaman statis untuk menu ini belum dibuat. '+'<br>Silahkan lakukan update di halaman statis."',admin_id=request.user.id);news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_n)[:1]
	news=news.get();optID=3;jenis=_T;get_topSection(siteID,context,_b);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis)
	if news:news.created_at=get_natural_datetime(news.created_at)
	context[_N]=jenis;context['news']=news;template_name=get_template(siteID);return render(request,f"{template_name}detail.html",context)
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def dokumen_ajax(request,idx):
	B='deskripsi';A='file_path';max=5;siteID=get_siteID(request)
	if idx==0:
		object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_X,B,_O,A,_P).order_by(_B)[:max];n=object_list.count()
		if max-n>0:object_list.union(dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_X,B,_O,A,_P).order_by(_B)[:max-n])
	elif idx==1:object_list=dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_X,B,_O,A,_P).order_by(_B)[:max]
	elif idx==2:object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_X,B,_O,A,_P).order_by(_B)
	if idx==0 or idx==1 or idx==2:
		for i in object_list:i[_P]=get_natural_datetime(i[_P]);i[_O]=naturalsize(i[_O]);i[A]=settings.MEDIA_URL+i[A]
		mData=list(object_list)
	else:mData=_D
	return JsonResponse(mData,safe=_m)
def satudata_ajax(request,idx):
	if idx==0 or idx==1:
		for i in object_list:i[_P]=get_natural_datetime(i[_P]);i[_O]=naturalsize(i[_O])
		mData=list(object_list)
	else:mData=_D
	return JsonResponse(mData,safe=_m)
def satudata_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	optID=2;context[_N]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);template_name=get_template(siteID);return render(request,f"{template_name}/satudata-result.html",context)
def dokumen_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_K]=_M%(request.get_host(),_I);return render(request,_L,context)
	optID=2;context[_N]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);template_name=get_template(siteID);return render(request,f"{template_name}/dokumen-result.html",context)
def get_template_id(site_id,is_frontend=_J):
	template=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list(_C,flat=_J)[:1];
	if template:return template[0]
	raise Http404(_p%_I)
def get_template(site_id,is_frontend=_J):
	template=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('rel_path',flat=_J)[:1];
	if template:return template[0]
	raise Http404(_p%_I)