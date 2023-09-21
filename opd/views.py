_s='opd/search-result.html'
_r='opd/detail.html'
_q='-updated_at'
_p='photo__berita__id'
_o='berita__id'
_n=False
_m='num_pages'
_l='jumlah'
_k='page_obj'
_j='page'
_i='-view_count'
_h='body'
_g='date2'
_f='date1'
_e='artikel'
_d='pengumuman'
_c='isi_berita'
_b='kategori__nama'
_a='nama'
_Z='menu'
_Y='feed1'
_X='?page=1'
_W='/search/'
_V='berita'
_U='photo__file_path'
_T='name'
_S='POST'
_R='updated_at'
_Q='jenis'
_P='/admin'
_O="Domain <b>%s</b> belum terdaftar, silahkan hubungi <br><a href='%s'>admin</a><br> untuk melakukan pendaftaran"
_N='account/error404.html'
_M='msg'
_L='size'
_K='admin__username'
_J='judul_seo'
_I='site__name'
_H='judul'
_G='feed2'
_F=True
_E='search'
_D='-id'
_C='id'
_B=None
_A='created_at'
import calendar,datetime,re
from easy_thumbnails.files import get_thumbnailer
import feedparser
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import OuterRef,Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.utils.html import strip_tags
from django.utils.safestring import SafeString
from django.utils.text import Truncator,slugify
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from humanize import naturalsize
from outbox_hitcount.views import get_statistic
from account.commonf import get_topFoto
from django_opd.commonf import get_natural_datetime
from opd.models import comment
from.import menus
from.forms import CommentForm
from.models import*
cache_item=dict()
cache_item[_Y]=_B
cache_item[_f]=_B
cache_item[_G]=_B
cache_item[_g]=_B
def get_siteID(request):
	if request:siteID=Site.objects.filter(domain=request.get_host()).values_list(_C,flat=_F);return siteID[0]if siteID else 0
	return 0
def get_comment(siteID,newsID,context):
	komentar=comment.objects.filter(site_id=siteID,post_id=newsID,active=_F).order_by(_D).values(_T,_h,_A)
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
def get_banner_all(siteID,context):banner=banner_all.objects.filter(site__id=siteID,status=Status.PUBLISHED).order_by(_D);context['banner_all']=banner
def get_topSection(siteID,context,active_menu):
	namaOPD=Site.objects.filter(id=siteID).values_list(_T,flat=_F)
	if namaOPD.count()>0:context['namaOPD']=namaOPD[0]
	mObjMenu=menus.ClsMenus();myMenu=menus.ClsMenus(siteID,_n);context[_Z]=myMenu.get_menus();context['activeMenuList']=myMenu.find_activeMenuList(active_menu);context['socialMedia']=social_media.objects.filter(site_id=siteID);logoTop=logo.objects.filter(site_id=siteID,position=logo.Position.TOP)
	if logoTop.count()>0:context['logoTop']=logoTop[0].photo
	bannerTop=banner.objects.filter(site_id=siteID,position=banner.Position.TOP)
	if bannerTop.count()>0:context['bannerTop']=bannerTop[0]
def get_bottomSection(siteID,context,optID):
	E='https://widget.kominfo.go.id/data/covid-19/gpr.xml';D='get from server Widget';C='get from server (RSS)';B='https://kominfo.go.id/content/rss/laporan_isu_hoaks';A='feed';logoBottom=logo.objects.filter(site_id=siteID,position=logo.Position.BOTTOM)
	if logoBottom.count()>0:context['logoBottom']=logoBottom[0].photo
	context['instansi']=instansi.objects.filter(site_id=siteID)[:1]
	if optID==1:context['agenda']=agenda.objects.filter(site_id=siteID).order_by(_D)[:5]
	context[A]=_B
	if cache_item[_Y]is _B:
		try:context[A]=feedparser.parse(B);cache_item[_Y]=context[A];cache_item[_f]=datetime.datetime.now();print(C)
		except:pass
	elif(datetime.datetime.now()-cache_item[_f]).seconds>36000:
		try:context[A]=feedparser.parse(B);cache_item[_Y]=context[A];cache_item[_f]=datetime.datetime.now();print(C)
		except:pass
	else:context[A]=cache_item[_Y];print('get from cached (RSS)')
	if optID==1:
		context[_G]=_B;skrg=datetime.datetime.now()
		if cache_item[_G]is _B:
			try:
				if not settings.DEBUG:print(D);context[_G]=feedparser.parse(E)
				else:context[_G]=''
				cache_item[_G]=context[_G];simpan=datetime.datetime.now();cache_item[_g]=simpan.hour*3600+simpan.minute*60+simpan.second
			except:pass
		elif skrg.hour*3600+skrg.minute*60+skrg.second-cache_item[_g]>36000:
			try:
				if not settings.DEBUG:print(D);context[_G]=feedparser.parse(E)
				else:context[_G]=''
				cache_item[_G]=context[_G];simpan=datetime.datetime.now();cache_item[_g]=simpan.hour*3600+simpan.minute*60+simpan.second
			except:pass
		else:print('get from cached Widget');context[_G]=cache_item[_G]
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
	context['tags']=tags.objects.filter(site__id=siteID).order_by(_a)
	if opt!=1:get_beritaTerbaru(siteID,context,3);get_beritaTerpopuler(siteID,context,3);get_pengumuman(siteID,context,3);get_artikel(siteID,context,3)
def get_beritaTerbaru(siteID,context,opt):
	B='beritaTerbaruAll';A='site__domain'
	if opt==1:maxNews=6
	elif opt==2:maxNews=100
	else:maxNews=3
	model_criteria={_o:OuterRef(_p)};subQry=get_topFoto(model_criteria);BeritaTerbaruLain=_B;BeritaTerbaruAll=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_I,_b,_H,_J,_c,_K,_A,A).order_by(_D).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:BeritaTerbaruLain=berita.objects.filter(status=Status.PUBLISHED).exclude(site_id=siteID).values(_C,_I,_b,_H,_J,_c,_K,_A,A).order_by(_D).distinct().annotate(foto=subQry)[:maxNews]
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
	model_criteria={_o:OuterRef(_p)};subQry=get_topFoto(model_criteria);BeritaTerpopulerLain=_B;BeritaQry=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
	if BeritaCount==0:BeritaCutOff=0
	else:BeritaCutOff=BeritaQry.order_by(_D).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
	BeritaTerpopulerAll=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_I,_b,_H,_J,_c,_K,_A).order_by(_i).distinct().annotate(foto=subQry)[:maxNews]
	if opt==1:
		BeritaQry=berita.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED);BeritaCount=BeritaQry.count()
		if BeritaCount==0:BeritaCutOff=0
		else:BeritaCutOff=BeritaQry.order_by(_D).values_list(_C)[min(maxNews,BeritaCount-1)];BeritaCutOff=BeritaCutOff[0]
		BeritaTerpopulerLain=BeritaQry.filter(id__gte=BeritaCutOff).values(_C,_I,_b,_H,_J,_c,_K,_A).order_by(_i).distinct().annotate(foto=subQry)[:maxNews]
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
	model_criteria={'pengumuman__id':OuterRef('photo__pengumuman__id')};subQry=get_topFoto(model_criteria);PengumumanLain=_B;PengumumanAll=pengumuman.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_I,_H,_J,A,_K,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxPengumuman]
	if opt==1:PengumumanLain=pengumuman.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_I,_H,_J,A,_K,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxPengumuman]
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
	model_criteria={'artikel__id':OuterRef('photo__artikel__id')};subQry=get_topFoto(model_criteria);ArtikelLain=_B;ArtikelAll=artikel.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_I,_H,_J,A,_K,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxArtikel]
	if opd==1:ArtikelLain=artikel.objects.exclude(site_id=siteID).filter(status=Status.PUBLISHED).values(_C,_I,_H,_J,A,_K,_A).order_by(_D).distinct().annotate(foto=subQry)[:maxArtikel]
	if ArtikelLain:ArtikelAll=ArtikelAll.union(ArtikelLain);context[B]=ArtikelAll;context['artikelLain']=ArtikelLain
	else:context[B]=ArtikelAll
	if ArtikelLain:
		for i in ArtikelLain:i[_A]=get_natural_datetime(i[_A])
	for i in ArtikelAll:i[_A]=get_natural_datetime(i[_A])
	return ArtikelAll
def get_beritaKategori(siteID,context,opt,kategori_slug):
	model_criteria={_o:OuterRef(_p)};subQry=get_topFoto(model_criteria);kategoriID=kategori.objects.filter(slug=kategori_slug).first();BeritaKategori=_B
	if kategoriID:BeritaKategori=berita.objects.filter(site_id=siteID,status=Status.PUBLISHED,kategori_id=kategoriID.id).values(_C,_I,_b,_H,_J,_c,_K,_A).order_by(_D).distinct().annotate(foto=subQry)
	return BeritaKategori
def get_hitCounter(request,obj,content_type):
	hit_count=HitCount.objects.get_for_object(obj);hit_count_response=HitCountMixin.hit_count(request,hit_count);content_type_id=ContentType.objects.filter(model=content_type).first()
	if content_type_id:
		hit_update=HitCount.objects.filter(object_pk=obj.id,content_type_id=content_type_id.id).values_list('hits',flat=_F)
		if hit_update.count()>0:obj.view_count=hit_update[0];obj.save()
def get_trending(siteID,context):
	maxData=7;trendingQry=berita.objects.filter(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_D).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending=trendingQry.filter(id__gte=trendingCutOff).order_by(_i).values_list(_C,_H,_J)[:maxData];trendingQry=berita.objects.exclude(site_id=siteID);trendingCount=trendingQry.count()
	if trendingCount==0:trendingCutOff=0
	else:trendingCutOff=trendingQry.order_by(_D).values_list(_C)[min(maxData,trendingCount-1)];trendingCutOff=trendingCutOff[0]
	trending_else=trendingQry.filter(id__gte=trendingCutOff).order_by(_i).values_list(_C,_H,_J)[:maxData]
	if trending_else:
		maxData_else=maxData-trending.count()
		if maxData_else>0:trending=trending.union(trending_else)
	context['trending']=trending
def get_galeryFoto(siteID,context,opd):
	A='galeryFoto'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryFoto=galery_foto.objects.filter(site_id=siteID).values(_C,_I,_H,_J,_K,_A,_U).order_by(_D)[:mMax]
	for i in galeryFoto:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureFoto']=galeryFoto[:1]
		if galeryFoto.count()<=1:context[A]=galeryFoto
		else:context[A]=galeryFoto[1:mMax-1]
	elif opd==2:return galeryFoto
def get_popup(siteID,context):context['popup']=popup.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_I,_K,_A,'status',_U).order_by(_q)[:1]
def get_galeryVideo(siteID,context,opd):
	A='galeryVideo'
	if opd==1:mMax=6
	elif opd==2:mMax=50
	galeryVideo=galery_video.objects.filter(site_id=siteID).values(_C,_I,_H,_K,_A,'embed','embed_video').order_by(_D)[:mMax]
	for i in galeryVideo:i[_A]=get_natural_datetime(i[_A])
	if opd==1:
		context['futureVideo']=galeryVideo[:1]
		if galeryVideo.count()<=1:context[A]=galeryVideo
		else:context[A]=galeryVideo[1:mMax-1]
	elif opd==2:return galeryVideo
def get_linkTerkait(siteID):linkTerkait=link_terkait.objects.filter(site__id=siteID).order_by(_C);return linkTerkait
def get_galeryLayanan(siteID,context):foto=galery_layanan.objects.filter(site_id=siteID,status=Status.PUBLISHED).order_by(_D)[:5];context['galeryLayanan']=foto
def get_meta(request,obj,context,jenis):
	H='photo';G='%s';F='news_desc';E='%s://%s/%s/%s';D='news_img_meta';C='news_url';B='news_img';A='https';print('jenis = ');print(jenis);context['site_name']='%s://%s'%(A,request.get_host())
	if jenis==_V:
		context[B]=berita.photo.through.objects.filter(berita__id=obj.id).values(_U);print("context['news_img'] = ");print(context[B]);context['news_tags']=berita.tags.through.objects.filter(berita__id=obj.id).values('tags__nama');a=berita.objects.filter(id=obj.id)
		for i in a:context[C]=E%(A,request.get_host(),_V,i.judul_seo);context[F]=Truncator(strip_tags(i.isi_berita)).chars(60).strip();context['news_title']=Truncator(strip_tags(i.isi_berita)).chars(30).strip();print("context['news_url'] = ");print(context[C])
		news_img_meta=berita.photo.through.objects.filter(berita__id=obj.id).order_by('photo__jenis')
		if news_img_meta.count()>0:options={_L:(100,100),'crop':_F};print(H,news_img_meta[0].photo);print(H,news_img_meta[0].photo.file_path);context[D]='%s://%s%s'%(A,request.get_host(),get_thumbnailer(news_img_meta[0].photo.file_path).get_thumbnail(options).url);print("context['news_img_meta'] = ");print(context[D])
	elif jenis==_d:
		context[B]=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id).values(_U);a=pengumuman.objects.filter(id=obj.id)
		for i in a:context[C]=E%(A,request.get_host(),_d,i.judul_seo);context[F]=SafeString(Truncator(i.isi_pengumuman).chars(160))
		news_img_meta=pengumuman.photo.through.objects.filter(pengumuman__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[D]=G%news_img_meta[0].photo
	elif jenis==_e:
		context[B]=artikel.photo.through.objects.filter(artikel__id=obj.id).values(_U);a=artikel.objects.filter(id=obj.id)
		for i in a:context[C]=E%(A,request.get_host(),_e,i.judul_seo);context[F]=SafeString(Truncator(i.isi_artikel).chars(160))
		news_img_meta=artikel.photo.through.objects.filter(artikel__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[D]=G%news_img_meta[0].photo
	elif jenis==_Z:
		context[B]=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id).values(_U);a=halaman_statis.objects.filter(id=obj.id)
		for i in a:context[C]=E%(A,request.get_host(),_Z,i.judul);context[F]=SafeString(Truncator(i.isi_halaman).chars(160))
		news_img_meta=halaman_statis.photo.through.objects.filter(halaman_statis__id=obj.id,photo__jenis=photo.Jenis.HIGHLIGHT1)
		if news_img_meta.count()>0:context[D]=G%news_img_meta[0].photo
def get_newsList(request,siteID,context,opt,section,jenis):
	news_per_page=6;mList=_B
	if section==_V:
		if jenis=='terbaru':mList=get_beritaTerbaru(siteID,context,opt)
		else:mList=get_beritaTerpopuler(siteID,context,opt)
	elif section==_d:mList=get_pengumuman(siteID,context,opt)
	elif section==_e:mList=get_artikel(siteID,context,opt)
	elif section=='kategori':mList=get_beritaKategori(siteID,context,opt,jenis)
	elif section=='galeri':
		if jenis=='video':mList=get_galeryVideo(siteID,context,opt)
		else:mList=get_galeryFoto(siteID,context,opt)
	elif section=='link':mList=get_linkTerkait(siteID)
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_j)
		if page_number is _B:page_number=1
		if page_number:context[_k]=paginator.get_page(page_number);context[_l]=paginator.page_range;context[_m]=paginator.num_pages
def index(request):
	context={};siteID=get_siteID(request)
	if not siteID:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	context[_Q]='index';active_menu='beranda';optID=1
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_middleSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_trending(siteID,context);get_banner_all(siteID,context);get_beritaTerbaru(siteID,context,optID);get_pengumuman(siteID,context,optID);get_beritaTerpopuler(siteID,context,optID);get_artikel(siteID,context,optID);get_galeryLayanan(siteID,context);obj=Site.objects.get(id=siteID);get_hitCounter(request,obj,'site');statistik=get_statistic(siteID,_F);context.update(statistik);get_popup(siteID,context);response=render(request,'opd/index.html',context);response.set_cookie(key=_T,value='my_value',samesite='None',secure=_F);return response
def detail(request,pid,jenis):
	A='email';context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	if jenis==_V:
		news=get_object_or_404(berita,judul_seo=pid);get_hitCounter(request,news,_V);mList=get_comment(siteID,news.id,context);news_per_page=3
		if mList is not _B:
			paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_j)
			if page_number is _B:page_number=1
			context[_k]=paginator.get_page(page_number);context[_l]=paginator.page_range;context[_m]=paginator.num_pages
		new_comment=_B
		if request.method==_S:
			comment_form=CommentForm(data=request.POST)
			if comment_form.is_valid():new_comment,created=comment.objects.get_or_create(site_id=siteID,name__iexact=request.POST.get(_T).strip(),body__iexact=request.POST.get(_h).strip(),defaults={'post':news,_h:request.POST.get(_h),_T:request.POST.get(_T),A:request.POST.get(A)})
		else:comment_form=CommentForm()
		context['new_comment']=new_comment;context['comment_form']=comment_form
	elif jenis==_d:news=get_object_or_404(pengumuman,judul_seo=pid);get_hitCounter(request,news,_d)
	elif jenis==_e:news=get_object_or_404(artikel,judul_seo=pid);get_hitCounter(request,news,_e)
	else:context[_M]='Halaman <b>%s</b> tidak ditemukan!'%pid;return render(request,_N,context)
	if news:news.created_at=get_natural_datetime(news.created_at)
	optID=3;context[_Q]=jenis;context['news']=news;get_topSection(siteID,context,jenis);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);statistik=get_statistic(siteID,_F);context.update(statistik);return render(request,_r,context)
def detail_list(request,section,jenis):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	optID=2;context[_Q]=jenis;context['section']=section;active_menu=jenis
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_newsList(request,siteID,context,optID,section,jenis);statistik=get_statistic(siteID,_F);context.update(statistik);return render(request,'opd/detail-list.html',context)
def search_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	optID=2;context[_Q]=_E;active_menu=_E
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);statistik=get_statistic(siteID,_F);context.update(statistik);context[_E]=pdata;mList=get_search_result(context,pdata);news_per_page=5
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_j)
		if page_number is _B:page_number=1
		context[_k]=paginator.get_page(page_number);context[_l]=paginator.page_range;context[_m]=paginator.num_pages
	return render(request,_s,context)
def tags_result(request,pdata):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	optID=2;context[_Q]=_E;active_menu=_E
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);statistik=get_statistic(siteID,_F);context.update(statistik);context[_E]=pdata;mList=get_tags_result(context,pdata);news_per_page=5
	if mList is not _B:
		paginator=Paginator(mList,news_per_page);page_number=request.GET.get(_j)
		if page_number is _B:page_number=1
		context[_k]=paginator.get_page(page_number);context[_l]=paginator.page_range;context[_m]=paginator.num_pages
	return render(request,_s,context)
def halaman_statis_akses(request,slug):
	A='-created_at';context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	if request.method==_S:
		pdata=request.POST.get(_E)
		if pdata:
			pdata=pdata.strip()
			if pdata!='':return redirect(_W+slugify(pdata)+_X)
	print('slug=',slug);menu_id=menu.objects.filter(href='menu/'+slug);print('count = ',menu_id.count())
	for i in menu_id:print(_Z,i.id,i.nama)
	mFoundID=0;mNama=''
	for i in menu_id:
		mFoundID=i.id;mNama=i.nama
		if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID,is_edited=1).order_by(A).exists():mFoundID=i.id;mNama=i.nama;break
	if mFoundID==0:
		for i in menu_id:
			if halaman_statis.objects.filter(menu_id=i.id,site_id=siteID).order_by(A).exists():mFoundID=i.id;mNama=i.nama;break
	news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_q)[:1];print('news [GET]= ');print(news)
	if not news:news=halaman_statis.objects.create(menu_id=mFoundID,site_id=siteID,judul=mNama,isi_halaman='Informasi tentang "'+mNama+'". Silahkan update di halaman <a target="_blank" href="/dashboard/halaman-statis/">Dashboard.<a>'+'<br><br><br><br>'+'"Halaman ini dibuat otomatis oleh sistem, karena halaman statis untuk menu ini belum dibuat. '+'<br>Silahkan lakukan update di halaman statis."',admin_id=request.user.id);news=halaman_statis.objects.filter(menu_id=mFoundID,site_id=siteID).order_by(_q)[:1];print('news [CREATE]= ');print(news)
	news=news.get();optID=3;jenis=_Z;get_hitCounter(request,news,'halaman_statis');get_topSection(siteID,context,_V);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);get_meta(request,news,context,jenis);statistik=get_statistic(siteID,_F);context.update(statistik)
	if news:news.created_at=get_natural_datetime(news.created_at)
	context[_Q]=jenis;context['news']=news;return render(request,_r,context)
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def dokumen_ajax(request,idx):
	B='deskripsi';A='file_path';max=5;siteID=get_siteID(request)
	if idx==0:
		object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_L,A,_R).order_by(_D)[:max];n=object_list.count()
		if max-n>0:object_list.union(dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_L,A,_R).order_by(_D)[:max-n])
	elif idx==1:object_list=dokumen.objects.exclude(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_L,A,_R).order_by(_D)[:max]
	elif idx==2:object_list=dokumen.objects.filter(site_id=siteID,status=Status.PUBLISHED).values(_C,_a,B,_L,A,_R).order_by(_D)
	if idx==0 or idx==1 or idx==2:
		for i in object_list:i[_R]=get_natural_datetime(i[_R]);i[_L]=naturalsize(i[_L]);i[A]=settings.MEDIA_URL+i[A]
		mData=list(object_list)
	else:mData=_B
	return JsonResponse(mData,safe=_n)
def satudata_ajax(request,idx):
	if idx==0 or idx==1:
		for i in object_list:i[_R]=get_natural_datetime(i[_R]);i[_L]=naturalsize(i[_L])
		mData=list(object_list)
	else:mData=_B
	return JsonResponse(mData,safe=_n)
def satudata_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	optID=2;context[_Q]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);statistik=get_statistic(siteID,_F);context.update(statistik);return render(request,'opd/satudata-result.html',context)
def dokumen_result(request):
	context={};siteID=get_siteID(request)
	if siteID==0:context[_M]=_O%(request.get_host(),_P);return render(request,_N,context)
	optID=2;context[_Q]=_E;active_menu=_E;get_topSection(siteID,context,active_menu);get_bottomSection(siteID,context,optID);get_sideBar(siteID,context,optID);statistik=get_statistic(siteID,_F);context.update(statistik);return render(request,'opd/dokumen-result.html',context)