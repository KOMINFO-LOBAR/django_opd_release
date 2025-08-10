_Ah=' Instansi)'
_Ag='Lainnya ('
_Af='not found'
_Ae='Menu tidak dapat diakses dari user Anda!'
_Ad='str_foto_path = '
_Ac='form_data_kategori'
_Ab='form_data'
_Aa='mGrandTotal'
_AZ='is_visibled'
_AY='pagination'
_AX='results'
_AW='search'
_AV='mFound = False '
_AU='mFound = True '
_AT='-jumlah'
_AS='admin'
_AR='word_count'
_AQ='tanggal'
_AP='jabatan'
_AO='/dashboard/pejabat'
_AN='auto_resize'
_AM='parent_id'
_AL='form_img'
_AK='photo_id'
_AJ='photo-str_file_path'
_AI='kode_post'
_AH='alamat'
_AG='siteid'
_AF='mChartNews'
_AE='mChartHit'
_AD='/dashboard/dashboard'
_AC='total_menu'
_AB='/dashboard/link-terkait'
_AA='/dashboard/menu'
_A9='photo'
_A8='email'
_A7='potential_duplicate_add'
_A6='%B %Y'
_A5='persen'
_A4='created_at'
_A3='isi_halaman'
_A2='deskripsi'
_A1='isi_artikel'
_A0='isi_pengumuman'
_z='isi_berita'
_y='-file_path'
_x='order_menu'
_w='parent__nama'
_v='photo__file_path'
_u='media/'
_t='jenis'
_s='highlight-editor'
_r='formset_img'
_q='file_path'
_p='text'
_o='terisi'
_n='parent'
_m='name'
_l='site_id'
_k='link'
_j='username'
_i='artikel'
_h='pengumuman'
_g='berita'
_f='save foto complete '
_e='status'
_d='total'
_c='-str_file_path'
_b='form_edit'
_a='Parameter Primary Key tidak ditemukan!'
_Z='Parameter Primary Key tidak tersedia'
_Y='save_add'
_X='-id'
_W='form_add'
_V='mode'
_U='form'
_T='save_edit'
_S='menu_aktif'
_R='namaOPD'
_Q='breadCrumb'
_P='/account/login'
_O='activeMenuList'
_N='add'
_M='edit'
_L='menu'
_K='POST'
_J=None
_I='form-'
_H='domain'
_G='judul'
_F='delete'
_E='nama'
_D='updated_at'
_C=False
_B=True
_A='id'
import calendar,io,os,re,unicodedata
from datetime import datetime,timezone
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core import serializers
from django.db.models import Count,F,OuterRef
from django.forms import formset_factory,modelformset_factory
from django.http import Http404,JsonResponse
from django.shortcuts import HttpResponse,get_object_or_404,redirect,render
from django.utils.text import Truncator,slugify
from hitcount.models import Hit,HitCount
from humanize import naturalsize
from PIL import Image
from.commonf import get_topFoto
from.forms import CustomUserCreationForm
from django_opd.commonf import get_natural_datetime
from opd import menus,models
from.import crypt_uuid4,forms,msgbox
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup as BS
mMsgBox=msgbox.ClsMsgBox()
User=get_user_model()
def get_menus(request,siteID,context,active_menu):
	D=context;E=request.user.id;print('user_id',E);C=User.objects.get(id=E);print('obj',C);A=C.groups.all()[:1];print('group_id',A)
	if A:A=A.get().id
	print('==',A)
	if not A:
		B=Group.objects.filter(name='Admin')
		if B:B=B.get();A=B.id;print('group',B);C.groups.add(B)
	if A:
		F=menus.Menus(menu_group=A,kinds=2);G=[]
		for H in F.get_menus():
			if H[_AZ]:G.append(H)
		D[_L]=G;I=active_menu.replace('_',' ');D[_O]=F.get_active_menu_by_name(I)
	else:print('Group ID Not Found!')
def unicode_to_string(value):B='ascii';A=value;A=str(A);A=unicodedata.normalize('NFKD',A).encode(B,'ignore').decode(B);return A
def redirect_to_login(request):
	if request.user.is_authenticated:return redirect(_AD)
	return redirect('/captcha/login')
def get_siteID(request):
	A=request;B=Site.objects.filter(domain=A.get_host()).values_list(_A,flat=_B)
	if B.count()==0:raise Http404("domain '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(A.get_host(),'/admin'))
	return B[0]
def get_namaOPD(pSiteID):
	A=Site.objects.filter(id=pSiteID).values_list(_m,flat=_B)[:1]
	if A.count()>0:A=A[0]
	return A
def add_months(sourcedate,months):B=sourcedate;A=B.month-1+months;C=B.year+A//12;A=A%12+1;D=min(B.day,calendar.monthrange(C,A)[1]);return datetime(C,A,D)
def get_hit_count(request):
	G=request;H=get_siteID(G);L=G.get_host();J=datetime.now();B=ContentType.objects.get(app_label='sites',model='site');B=B.id if B else _J;C=HitCount.objects.filter(content_type_id=B,object_pk=H).first();C=C.id if C else _J;I=[];E={};D='';F=0
	for K in range(7):
		A=add_months(J,K-6)
		if H==1:F=Hit.objects.filter(created__year=A.year,created__month=A.month).count()
		else:F=Hit.objects.filter(hitcount_id=C,created__year=A.year,created__month=A.month).count()
		I.append(F)
		if D!='':D+=','
		D+=A.strftime('%B')
	E['bulan']=D;E['hit']=I;return E
def get_news_count(request):
	C=get_siteID(request);K=datetime.now();H=[];I=[];J=[];B={};D='';E=0;F=0;G=0
	for L in range(7):
		A=add_months(K,L-6)
		if C==1:E=models.berita.objects.filter(created_at__year=A.year,created_at__month=A.month).count();F=models.pengumuman.objects.filter(created_at__year=A.year,created_at__month=A.month).count();G=models.artikel.objects.filter(created_at__year=A.year,created_at__month=A.month).count()
		else:E=models.berita.objects.filter(site_id=C,created_at__year=A.year,created_at__month=A.month).count();F=models.pengumuman.objects.filter(site_id=C,created_at__year=A.year,created_at__month=A.month).count();G=models.artikel.objects.filter(site_id=C,created_at__year=A.year,created_at__month=A.month).count()
		H.append(E);I.append(F);J.append(G)
		if D!='':D+=','
		D+=A.strftime('%B')
	B['bulan']=D;B[_g]=H;B[_h]=I;B[_i]=J;return B
def cek_user(request):
	A=request
	if not models.instansi.objects.filter(site_id=get_siteID(A),admin__id=A.user.id).exists():raise Http404("user <b>%s</b> tidak di temukan di domain <b>%s</b>. <a href='%s' onclick='%s'>Logout</a>"%(A.user.username,A.get_host(),'javascript:void(0)','login_again()'))
@login_required(login_url=_P)
def dashboard(request):A=request;cek_user(A);D=get_siteID(A);B=menus.ClsMenus(D,_B);F=get_hit_count(A);G=get_news_count(A);C='analytics';H=models.menu.objects.filter(nama=C,is_admin_menu=_B);E={};E={_L:B.get_menus(),_Q:B.create_breadCrumb(C),_O:B.find_activeMenuList(C),_R:get_namaOPD(D),_S:H,_AE:F,_AF:G};return render(A,'account/dashboard.html',E)
@login_required(login_url=_P)
def dashboard_detail(request):
	B=request;cek_user(B);C=get_siteID(B);E=menus.ClsMenus(C,_B);I=models.berita.objects.exclude(site_id=1).count();J=models.artikel.objects.exclude(site_id=1).count();K=models.pengumuman.objects.exclude(site_id=1).count();G=models.Site.objects.get(id=C);L={_A:G.id,_p:G.domain};D={};A=models.instansi.objects.filter(site_id=C)
	if A:
		A=A.get()
		if A.kategori:D={_A:A.kategori.id,_p:A.kategori.nama}
	if not D:A=models.instansi_kategori.objects.get(id=1);D={_A:A.id,_p:A.nama}
	print('form_data_kategori = ');print(D);M=get_hit_count(B);N=get_news_count(B);F='monitoring';O=models.menu.objects.filter(nama=F,is_admin_menu=_B);H={};H={_L:E.get_menus(),_Q:E.create_breadCrumb(F),_O:E.find_activeMenuList(F),_R:get_namaOPD(C),_S:O,_AE:M,_AF:N,_Aa:I+K+J,_AG:C,_Ab:L,_Ac:D};return render(B,'account/dashboard-detail.html',H)
@login_required(login_url=_P)
def dashboard_content_count(request):
	C=request;cek_user(C);D=get_siteID(C);F=menus.ClsMenus(D,_B);K=models.berita.objects.exclude(site_id=1).count();L=models.artikel.objects.exclude(site_id=1).count();M=models.pengumuman.objects.exclude(site_id=1).count();H=models.Site.objects.get(id=D);N={_A:H.id,_p:H.domain};B=datetime.now();print(f"Init Data: {B.month}.{B.year}",B.strftime(_A6));I={_A:f"{B.month}.{B.year}",_p:B.strftime(_A6)};print('form_data_month = ');print(I);E={};A=models.instansi.objects.filter(site_id=D)
	if A:
		A=A.get()
		if A.kategori:E={_A:A.kategori.id,_p:A.kategori.nama}
	if not E:A=models.instansi_kategori.objects.get(id=1);E={_A:A.id,_p:A.nama}
	O=get_hit_count(C);P=get_news_count(C);G='content count';Q=models.menu.objects.filter(nama=G,is_admin_menu=_B);J={};J={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_O:F.find_activeMenuList(G),_R:get_namaOPD(D),_S:Q,_AE:O,_AF:P,_Aa:K+M+L,_AG:D,_Ab:N,'form_data_month':I,_Ac:E};return render(C,'account/dashboard-content-count.html',J)
def register(request):
	A=request
	if A.method==_K:
		B=CustomUserCreationForm(A.POST)
		if B.is_valid():C=B.save();messages.info(A,mMsgBox.get(_Y,A.POST.get(_j)));return redirect(_P)
	else:B=forms.CustomUserCreationForm(label_suffix='')
	return render(A,'account/register.html',{_U:B})
@login_required(login_url=_P)
def social_media(request,mode='',pk=''):
	H='/dashboard/social-media';C=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_J
	if C==_M or C==_F:
		if pk=='':return HttpResponse(_Z)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_a)
		J=models.social_media.objects.filter(site_id=E,id=I)
	if C==_N:
		if A.method==_K:
			B=forms.SocialMediaForm(A.POST,label_suffix='')
			if B.is_valid():
				if models.social_media.objects.filter(site_id=E,link=A.POST.get(_k)).exists():messages.info(A,mMsgBox.get(_A7,A.POST.get(_k)))
				else:
					L=models.social_media.objects.create(site_id=E,jenis=A.POST.get(_t),link=A.POST.get(_k))
					if L:messages.info(A,mMsgBox.get(_Y,A.POST.get(_t)))
					return redirect(H)
		else:B=forms.SocialMediaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_M:
		D=get_object_or_404(J)
		if A.method==_K:
			B=forms.SocialMediaForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_t)));return redirect(H)
		else:B=forms.SocialMediaForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif C==_F:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_F,D.jenis));return redirect(H)
	G='social media';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_O:F.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(E),_S:M};return render(A,'account/social-media.html',N)
@login_required(login_url=_P)
def instansi(request,mode='',pk=''):
	I='/dashboard/instansi';C=mode;A=request;cek_user(A);D=get_siteID(A);E=menus.ClsMenus(D,_B);B=_J
	if C==_M:
		if pk=='':return HttpResponse(_Z)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_a)
		K=models.instansi.objects.filter(site_id=D,id=H)
	if C==_N:
		if A.method==_K:
			B=forms.InstansiForm(A.POST,label_suffix='')
			if B.is_valid():
				L=models.User.objects.get(id=A.user.id);M,N=models.instansi.objects.update_or_create(site_id=D,defaults={_E:A.POST.get(_E),_AH:A.POST.get(_AH),'telp':A.POST.get('telp'),_A8:A.POST.get(_A8),_AI:A.POST.get(_AI)});M.admin.add(L)
				if N:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(I)
		else:B=forms.InstansiForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_M:
		F=get_object_or_404(K)
		if A.method==_K:
			B=forms.InstansiForm(A.POST,instance=F,label_suffix='')
			if B.is_valid():F.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(I)
		else:B=forms.InstansiForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_b))
	G='instansi';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:E.get_menus(),_Q:E.create_breadCrumb(G),_O:E.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(D),_S:O};return render(A,'account/instansi.html',P)
@login_required(login_url=_P)
def logo(request,mode='',pk=''):
	K='logo';J='Logo ';C='logo-position';A=request;cek_user(A);B=get_siteID(A);D=menus.ClsMenus(B,_B);E=_J;F=_J
	if mode==_N:
		if A.method==_K:
			E=forms.LogoForm(A.POST);F=forms.PhotoForm(A.POST)
			if A.POST.get(C).upper()=='TOP':H=models.photo.Jenis.LOGO_TOP
			else:H=models.photo.Jenis.LOGO_BOTTOM
			I=A.POST.get(_AJ)
			if I:
				L=I.replace(_u,'');M,N=models.photo.objects.update_or_create(site_id=B,jenis=H,defaults={_q:L});Q,R=models.logo.objects.update_or_create(site_id=B,position=A.POST.get(C),defaults={_AK:M.id})
				if N:messages.info(A,mMsgBox.get(_Y,J+A.POST.get(C)))
				else:messages.info(A,mMsgBox.get(_T,J+A.POST.get(C)))
			return redirect('/dashboard/logo')
		else:E=forms.LogoForm(label_suffix='',prefix=K);F=forms.PhotoForm(label_suffix='',prefix=_A9);messages.info(A,mMsgBox.get(_W))
	G=K;O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:D.get_menus(),_Q:D.create_breadCrumb(G),_O:D.find_activeMenuList(G),_V:mode,_U:E,_AL:F,_R:get_namaOPD(B),_S:O};return render(A,'account/logo.html',P)
@login_required(login_url=_P)
def banner(request,mode='',pk=''):
	J='banner';A=request;cek_user(A);C=get_siteID(A);E=menus.ClsMenus(C,_B);F=_J;G=_J
	if mode==_N:
		if A.method==_K:
			F=forms.BannerForm(A.POST);G=forms.PhotoForm(A.POST);B=A.POST.get('banner-str_banner_position')
			if B=='bottom':D=models.photo.Jenis.BANNER_BOTTOM
			elif B=='middle1':D=models.photo.Jenis.BANNER_MIDDLE1
			elif B=='middle2':D=models.photo.Jenis.BANNER_MIDDLE2
			else:D=models.photo.Jenis.BANNER_TOP
			H=A.POST.get(_AJ);print(_Ad);print(H)
			if H:
				K=H.replace(_u,'');L,M=models.photo.objects.update_or_create(site_id=C,jenis=D,defaults={_q:K});P,Q=models.banner.objects.update_or_create(site_id=C,position=B,defaults={_AK:L.id,_k:A.POST.get('banner-link')})
				if M:messages.info(A,mMsgBox.get(_Y,B))
				else:messages.info(A,mMsgBox.get(_T,B))
			return redirect('/dashboard/banner')
		else:F=forms.BannerForm(label_suffix='',prefix=J);G=forms.PhotoForm(label_suffix='',prefix=_A9);messages.info(A,mMsgBox.get(_W))
	I=J;N=models.menu.objects.filter(nama=I,is_admin_menu=_B);O={_L:E.get_menus(),_Q:E.create_breadCrumb(I),_O:E.find_activeMenuList(I),_V:mode,_U:F,_AL:G,_R:get_namaOPD(C),_S:N};return render(A,'account/banner.html',O)
def menu_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.menu.objects.filter(is_master_menu=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('menu_refresh'));return redirect(_AA)
def menu_update_visibled(request,pk,is_visible):
	A=models.Site.objects.get(id=get_siteID(request));B=models.menu.objects.get(id=pk)
	if is_visible:B.site.add(A)
	else:B.site.remove(A)
	return HttpResponse('True')
def menu_is_have_child(menu_id):return models.menu.objects.filter(parent__id=menu_id).exists()
@login_required(login_url=_P)
def menu(request,mode='',pk=''):
	U='delete_fail';T='master_menu';S='is_master_menu';D=mode;A=request;cek_user(A);E=get_siteID(A);J=menus.ClsMenus(E,_B);C=_J;L=_J;F=_J
	if D=='':V=menus.ClsMenus(E,_C,_B);L=V.get_menus()
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		W=crypt_uuid4.ClsCryptUuid4();M=W.dec_text(pk)
		if M=='':return HttpResponse(_a)
		N=models.menu.objects.filter(site__id=E,id=M)
	if D==_N or D==_n:
		if D==_n:F=pk
		if A.method==_K:
			C=forms.MenuForm(A.POST,label_suffix='')
			if C.is_valid():
				G=models.Site.objects.get(id=E);F=A.POST.get(_n)
				if not F:F=_J
				O=_B;P=models.menu.objects.filter(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F).values_list(S,flat=_B)
				if P.count()>0:
					if P[0]==_B:messages.info(A,mMsgBox.get(T));C=forms.MenuForm(label_suffix='');O=_C
				if O:
					X,Y=models.menu.objects.update_or_create(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F,defaults={_E:A.POST.get(_E),'href':'menu/'+slugify(A.POST.get(_E)),'icon':A.POST.get('icon'),_x:A.POST.get(_x),_AZ:_B,'is_statis_menu':_B});X.site.add(G)
					if Y:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
					return redirect(_AA)
		else:C=forms.MenuForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		B=get_object_or_404(N)
		if A.method==_K:
			C=forms.MenuForm(A.POST,instance=B,label_suffix='')
			if A.POST.get(_n)==str(B.id):messages.info(A,mMsgBox.get('circular_menu'));C=forms.MenuForm(instance=B,label_suffix='')
			elif A.POST.get(S):messages.info(A,mMsgBox.get(T));C=forms.MenuForm(instance=B,label_suffix='')
			elif C.is_valid():B=C.save(commit=_C);B.is_statis_menu=1;B.is_visibled=1;B.save();G=models.Site.objects.get(id=E);B.site.add(G);messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(_AA)
		else:C=forms.MenuForm(instance=B,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif D==_F:
		B=get_object_or_404(N);Z=models.halaman_statis.objects.filter(site_id=E,menu_id=B.id);Q=_C;R=''
		for H in Z:
			if H.is_edited:R=H.judul;Q=_B;break
		if Q:messages.info(A,mMsgBox.get(U,'Halaman Statis > '+R))
		elif menu_is_have_child(B.id):messages.info(A,mMsgBox.get(U,'Sub Menu Lain (Sebagai Parent Menu)'))
		else:
			a=models.Site.objects.get(id=E);B.site.remove(a);I=models.halaman_statis.objects.filter(site_id=E,menu_id=B.id)
			for H in I:H.delete()
			I=models.menu.objects.get(id=B.id)
			if I.site.count()==0:I.delete()
			messages.info(A,mMsgBox.get(_F,B.nama))
		return redirect(_AA)
	K=_L;b=models.menu.objects.filter(nama=K,is_admin_menu=_B);c={_L:J.get_menus(),_Q:J.create_breadCrumb(K),_O:J.find_activeMenuList(K),_V:D,_U:C,'menu_master':L,_AM:F,_R:get_namaOPD(E),_S:b};return render(A,'account/menu.html',c)
def delete_photo(request):
	print('inside delete photo');C=range(3)
	for B in C:
		A=request.POST.get('file_path_'+str(B));print(A)
		if A!='':
			if os.path.isfile(A):os.remove(A);print('remove photo success '+str(B))
	return HttpResponse('OKE')
def upload_photo(request,width,height):
	O='JPEG';N='RGBA';M='image/png';J='/';I='.jpg';G=request;A=G.FILES.get(_A9);H=G.POST.get('old_photo')
	if H:
		if os.path.isfile(H):os.remove(H);print('remove photo success')
	P=get_siteID(G);Q=Image.open(io.BytesIO(A.read()));B=Q.resize((width,height),Image.Resampling.LANCZOS);F=datetime.now();R=str(P)+'-'+F.strftime('%Y%m%d-%H%M%S-%f');S=F.strftime('%Y');T=F.strftime('%m');U=F.strftime('%d')
	if A.content_type=='image/gif':C='.gif'
	elif A.content_type=='image/jpeg':C=I
	elif A.content_type=='image/jpg':C=I
	elif A.content_type==M:C=I
	elif A.content_type=='image/bmp':C='.bmp'
	else:C='.ief'
	V=settings.BASE_DIR;K=settings.MEDIA_ROOT;print('base_dir');print(V);D='crop/'+S+J+T+J+U+J;print('path');print(D);E=os.path.join(K,D);W=os.makedirs(E,exist_ok=_B);D=D+R+C;E=os.path.join(K,D)
	if A.content_type==M:
		B.load();L=Image.new('RGB',B.size,(255,255,255))
		if B.mode==N:print(N);L.paste(B,mask=B.getchannel('A'));L.save(E,O,quality=80,optimize=_B)
		else:print('NON RGBA');B.save(E,O,quality=80,optimize=_B)
	else:B.save(E,quality=80,optimize=_B)
	return HttpResponse(D)
def get_photo_kind(idx):
	B=idx;A=_J
	if B==0:A=models.photo.Jenis.HIGHLIGHT1
	elif B==1:A=models.photo.Jenis.HIGHLIGHT2
	elif B==2:A=models.photo.Jenis.HIGHLIGHT3
	return A
def save_photo_slideshow(idx,site_id,photo_id,str_foto_path):
	C=photo_id;B=site_id;print('Begin INSPECT');D=get_photo_kind(idx);print('mode add/edit PHOTO IDs == ');print(C);E=str_foto_path;print('str_foto_path_replace');print(E);print(_t);print(D);print(_AG);print(B)
	if C:A=models.photo.objects.get(id=C);A.site_id=B;A.jenis=D;A.file_path=E;A.save();print('[save_photo_slideshow] - Update foto complete')
	else:A=models.photo.objects.create(site_id=B,jenis=D,file_path=E);print('[save_photo_slideshow] - save foto complete')
	print('END INSPECT');return A
def save_tags(tag_list,obj_master):
	C=obj_master;B=tag_list;D=models.berita.tags.through.objects.filter(berita_id=C.id)
	if D:D.delete()
	A=0
	while A<len(B):E=models.tags.objects.get(id=B[A]);C.tags.add(E);A+=1
@login_required(login_url=_P)
def berita(request,mode='',pk='',photoID=''):
	Z='/dashboard/berita';R=photoID;J=mode;A=request;cek_user(A);C=get_siteID(A);V=menus.ClsMenus(C,_B);E=_J;H=_J;R=[];S=_B
	if J==_M or J==_F:
		if pk=='':return HttpResponse(_Z)
		c=crypt_uuid4.ClsCryptUuid4();T=c.dec_text(pk)
		if T=='':return HttpResponse(_a)
		a=models.berita.objects.filter(site_id=C,id=T);M=models.berita.photo.through.objects.filter(berita__site=C,berita__id=T)
		for B in M:
			if B.photo.jenis!=_s:R.append(B.photo.id)
	elif J==_N:L=formset_factory(forms.PhotoForm,extra=3)
	if J==_N:
		if A.method==_K:
			E=forms.BeritaForm(A.POST)
			if S:H=L(A.POST,A.FILES)
			else:H=L(A.POST)
			if E.is_valid():
				D=A.POST.get(_G);F=A.POST.get(_z)
				if not D.isascii():print('is unicode');D=unicode_to_string(D)
				print('judul=',D)
				if not F.isascii():print('isi berita is contain unicode');F=unicode_to_string(F)
				print('isi berita =',F);U=models.berita.objects.create(site_id=C,judul=D,admin_id=A.user.id,kategori_id=A.POST.get('kategori'),isi_berita=F,status=A.POST.get(_e));W=A.POST.getlist('tags');save_tags(W,U);B=0
				for d in H:
					if S:
						N=A.FILES.get(_I+str(B)+_y)
						if N:
							K=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,K,N)
							if G:U.photo.add(G)
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:
							K=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,K,O)
							if G:U.photo.add(G)
					B+=1
				set_log_all(C,_B)
				if U:messages.info(A,mMsgBox.get(_Y,D))
				return redirect(Z)
		else:E=forms.BeritaForm(label_suffix='');H=L();messages.info(A,mMsgBox.get(_W))
	elif J==_M:
		P=get_object_or_404(a);L=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(R))
		if A.method==_K:
			E=forms.BeritaForm(A.POST,instance=P);H=L(A.POST)
			if E.is_valid():
				F=E.cleaned_data.get(_z)
				if not F.isascii():F=unicode_to_string(F)
				D=E.cleaned_data.get(_G)
				if not D.isascii():D=unicode_to_string(D)
				I=E.save(commit=_C);I.judul=D;I.isi_berita=F;I.site_id=C;I.admin_id=A.user.id;I.save();W=A.POST.getlist('tags');save_tags(W,I);B=0
				for d in H:
					if S:
						N=A.FILES.get(_I+str(B)+_y)
						if N:K=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,K,N);I.photo.add(G);print(_f+str(B))
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:K=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,K,O);I.photo.add(G);print(_f+str(B))
					B+=1
				set_log_all(C,_B);messages.info(A,mMsgBox.get(_T,D));return redirect(Z)
		else:E=forms.BeritaForm(instance=P,label_suffix='');H=L(queryset=models.photo.objects.filter(id__in=R));messages.info(A,mMsgBox.get(_b))
	elif J==_F:
		for B in M:
			Q=models.photo.objects.get(id=B.photo.id)
			if Q.file_path:
				if os.path.exists(Q.file_path.path):
					try:
						X=Image.open(Q.file_path.path);X.verify()
						if X:X.close()
					except Exception as e:print(f"{Q.file_path.path} is not a valid image. Error: {e}")
			Q.delete()
		M=models.berita.photo.through.objects.filter(berita__site=C,berita__id=T)
		if M:M.delete()
		P=get_object_or_404(a);P.delete();set_log_all(C,_B);messages.info(A,mMsgBox.get(_F,P.judul));return redirect(Z)
	Y=_g;f=models.menu.objects.filter(nama=Y,is_admin_menu=_B);b={};b={_L:V.get_menus(),_Q:V.create_breadCrumb(Y),_O:V.find_activeMenuList(Y),_V:J,_U:E,_r:H,_R:get_namaOPD(C),_S:f,_AN:S};return render(A,'account/berita.html',b)
@login_required(login_url=_P)
def kategori(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_J
	if mode==_N:
		if A.method==_K:
			B=forms.KategoriForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.kategori.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect('/dashboard/kategori')
		else:B=forms.KategoriForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='kategori';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_O:D.find_activeMenuList(E),_V:mode,_U:B,_R:get_namaOPD(C),_S:I};return render(A,'account/kategori.html',J)
@login_required(login_url=_P)
def tags(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_J
	if mode==_N:
		if A.method==_K:
			B=forms.TagsForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.tags.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect('/dashboard/tags')
		else:B=forms.TagsForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='tags';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_O:D.find_activeMenuList(E),_V:mode,_U:B,_R:get_namaOPD(C),_S:I};return render(A,'account/tags.html',J)
@login_required(login_url=_P)
def pengumuman(request,mode='',pk=''):
	a='Pengumuman';X='/dashboard/pengumuman';I=mode;A=request;cek_user(A);C=get_siteID(A);T=menus.ClsMenus(C,_B);D=_J;H=_J;U=[];Q=_B
	if I==_M or I==_F:
		if pk=='':return HttpResponse(_Z)
		b=crypt_uuid4.ClsCryptUuid4();R=b.dec_text(pk)
		if R=='':return HttpResponse(_a)
		Y=models.pengumuman.objects.filter(site_id=C,id=R);M=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=R)
		for B in M:
			if B.photo.jenis!=_s:U.append(B.photo.id)
	elif I==_N:L=formset_factory(forms.PhotoForm,extra=3)
	if I==_N:
		if A.method==_K:
			D=forms.PengumumanForm(A.POST)
			if Q:H=L(A.POST,A.FILES)
			else:H=L(A.POST)
			if D.is_valid():
				E=A.POST.get(_G);F=A.POST.get(_A0)
				if not E.isascii():E=unicode_to_string(E)
				if not F.isascii():F=unicode_to_string(F)
				V=models.pengumuman.objects.create(site_id=C,judul=E,admin_id=A.user.id,isi_pengumuman=F,status=A.POST.get(_e));B=0
				for c in H:
					if Q:
						N=A.FILES.get(_I+str(B)+_y)
						if N:
							J=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,J,N)
							if G:V.photo.add(G)
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:
							J=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,J,O)
							if G:V.photo.add(G);print(_f+str(B))
					B+=1
				if V:messages.info(A,mMsgBox.get(_Y,a))
				return redirect(X)
		else:D=forms.PengumumanForm(label_suffix='');H=L();messages.info(A,mMsgBox.get(_W))
	elif I==_M:
		P=get_object_or_404(Y);L=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(U))
		if A.method==_K:
			D=forms.PengumumanForm(A.POST,instance=P);H=L(A.POST)
			if D.is_valid():
				F=D.cleaned_data.get(_A0)
				if not F.isascii():F=unicode_to_string(F)
				E=D.cleaned_data.get(_G)
				if not E.isascii():E=unicode_to_string(E)
				K=D.save(commit=_C);K.judul=E;K.isi_pengumuman=F;K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for c in H:
					if Q:
						N=A.FILES.get(_I+str(B)+_y)
						if N:J=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,J,N);K.photo.add(G);print(_f+str(B))
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:J=A.POST.get(_I+str(B)+_X);G=save_photo_slideshow(B,C,J,O);K.photo.add(G);print(_f+str(B))
					B+=1
			messages.info(A,mMsgBox.get(_T,a));return redirect(X)
		else:D=forms.PengumumanForm(instance=P,label_suffix='');H=L(queryset=models.photo.objects.filter(id__in=U));messages.info(A,mMsgBox.get(_b))
	elif I==_F:
		for B in M:
			S=models.photo.objects.get(id=B.photo.id)
			if S.file_path:
				if os.path.isfile(S.file_path.path):
					Z=Image.open(S.file_path.path)
					if Z:Z.close()
			S.delete()
		M=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=R)
		if M:M.delete()
		P=get_object_or_404(Y);P.delete();messages.info(A,mMsgBox.get(_F,P.judul));return redirect(X)
	W=_h;d=models.menu.objects.filter(nama=W,is_admin_menu=_B);e={_L:T.get_menus(),_Q:T.create_breadCrumb(W),_O:T.find_activeMenuList(W),_V:I,_U:D,_r:H,_R:get_namaOPD(C),_S:d,_AN:Q};return render(A,'account/pengumuman.html',e)
@login_required(login_url=_P)
def artikel(request,mode='',pk=''):
	X='/dashboard/artikel';I=mode;A=request;cek_user(A);C=get_siteID(A);T=menus.ClsMenus(C,_B);D=_J;G=_J;U=[];Q=_B
	if I==_M or I==_F:
		if pk=='':return HttpResponse(_Z)
		a=crypt_uuid4.ClsCryptUuid4();R=a.dec_text(pk)
		if R=='':return HttpResponse(_a)
		Y=models.artikel.objects.filter(site_id=C,id=R);M=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=R)
		for B in M:
			if B.photo.jenis!=_s:U.append(B.photo.id)
	elif I==_N:L=formset_factory(forms.PhotoForm,extra=3)
	if I==_N:
		if A.method==_K:
			D=forms.ArtikelForm(A.POST)
			if Q:G=L(A.POST,A.FILES)
			else:G=L(A.POST)
			print('form.is_valid()',D.is_valid())
			if D.is_valid():
				E=A.POST.get(_G);F=A.POST.get(_A1)
				if not E.isascii():E=unicode_to_string(E)
				if not F.isascii():F=unicode_to_string(F)
				V=models.artikel.objects.create(site_id=C,judul=E,admin_id=A.user.id,isi_artikel=F,status=A.POST.get(_e));B=0
				for b in G:
					if Q:
						N=A.FILES.get(_I+str(B)+_y)
						if N:
							J=A.POST.get(_I+str(B)+_X);H=save_photo_slideshow(B,C,J,N)
							if H:V.photo.add(H)
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:J=A.POST.get(_I+str(B)+_X);H=save_photo_slideshow(B,C,J,O);V.photo.add(H);print(_f+str(B))
					B+=1
				if V:messages.info(A,mMsgBox.get(_Y,A.POST.get(_G)))
				return redirect(X)
		else:D=forms.ArtikelForm(label_suffix='');G=L();messages.info(A,mMsgBox.get(_W))
	elif I==_M:
		P=get_object_or_404(Y);L=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(U))
		if A.method==_K:
			D=forms.ArtikelForm(A.POST,instance=P);G=L(A.POST)
			if D.is_valid():
				F=D.cleaned_data.get(_A1)
				if not F.isascii():F=unicode_to_string(F)
				E=D.cleaned_data.get(_G)
				if not E.isascii():E=unicode_to_string(E)
				K=D.save(commit=_C);K.judul=E;K.isi_artikel=F;K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for b in G:
					if Q:
						N=A.FILES.get(_I+str(B)+_y)
						if N:J=A.POST.get(_I+str(B)+_X);H=save_photo_slideshow(B,C,J,N);K.photo.add(H);print(_f+str(B))
					else:
						O=A.POST.get(_I+str(B)+_c)
						if O:J=A.POST.get(_I+str(B)+_X);H=save_photo_slideshow(B,C,J,O);K.photo.add(H);print(_f+str(B))
					B+=1
			messages.info(A,mMsgBox.get(_T,'Artikel'));return redirect(X)
		else:D=forms.ArtikelForm(instance=P,label_suffix='');G=L(queryset=models.photo.objects.filter(id__in=U));messages.info(A,mMsgBox.get(_b))
	elif I==_F:
		for B in M:
			S=models.photo.objects.get(id=B.photo.id)
			if S.file_path:
				if os.path.isfile(S.file_path.path):
					Z=Image.open(S.file_path.path)
					if Z:Z.close()
			S.delete()
		M=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=R)
		if M:M.delete()
		P=get_object_or_404(Y);P.delete();messages.info(A,mMsgBox.get(_F,P.judul));return redirect(X)
	W=_i;c=models.menu.objects.filter(nama=W,is_admin_menu=_B);d={_L:T.get_menus(),_Q:T.create_breadCrumb(W),_O:T.find_activeMenuList(W),_V:I,_U:D,_r:G,_R:get_namaOPD(C),_S:c,_AN:Q};return render(A,'account/artikel.html',d)
def pejabat_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.pejabat.objects.filter(is_default=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('pejabat_refresh'));return redirect(_AO)
@login_required(login_url=_P)
def pejabat(request,mode='',pk=''):
	C=mode;A=request;cek_user(A);B=get_siteID(A);F=menus.ClsMenus(B,_B);D=_J;G=_J
	if C==_M or C==_F:
		if pk=='':return HttpResponse(_Z)
		M=crypt_uuid4.ClsCryptUuid4();J=M.dec_text(pk)
		if J=='':return HttpResponse(_a)
		N=models.pejabat.objects.filter(site__id=B,id=J)
	if C==_N:
		if A.method==_K:
			D=forms.PejabatForm(A.POST);G=forms.PhotoForm(A.POST);O=models.photo.Jenis.PEJABAT_OPD
			if D.is_valid():
				K=A.POST.get(_AJ)
				if K:
					P=K.replace(_u,'');Q,R=models.photo.objects.update_or_create(site_id=B,jenis=O,defaults={_q:P});print('siteID',B);print('models.pejabat.Position.PEJABAT_OPD',models.pejabat.Position.PEJABAT_OPD);L,S=models.pejabat.objects.update_or_create(site__id=B,jabatan_index=models.pejabat.Position.PEJABAT_OPD,defaults={_AK:Q.id,_E:A.POST.get(_E),_AP:A.POST.get(_AP),'admin_id':A.user.id,'is_default':0});print(L,S);T=models.Site.objects.get(id=B);L.site.add(T)
					if R:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(_AO)
		else:D=forms.PejabatForm(label_suffix='');G=forms.PhotoForm(label_suffix='',prefix=_A9);messages.info(A,mMsgBox.get(_W))
	elif C==_F:
		E=get_object_or_404(N);print('post = ');print(E.photo.id);H=models.photo.objects.filter(id=E.photo.id);print('foto = ');print(H)
		if H:H.delete()
		E.delete();messages.info(A,mMsgBox.get(_F,E.nama));return redirect(_AO)
	I='pejabat';U=models.menu.objects.filter(nama=I,is_admin_menu=_B);V={_L:F.get_menus(),_Q:F.create_breadCrumb(I),_O:F.find_activeMenuList(I),_V:C,_U:D,_AL:G,_R:get_namaOPD(B),_S:U};return render(A,'account/pejabat.html',V)
def link_terkait_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.link_terkait.objects.all()
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('link_terkait_refresh'));return redirect(_AB)
@login_required(login_url=_P)
def link_terkait(request,mode='',pk=''):
	D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_J
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_a)
		I=models.link_terkait.objects.filter(site__id=E,id=H)
	if D==_N:
		if A.method==_K:
			B=forms.LinkTerkaitForm(A.POST,label_suffix='')
			if B.is_valid():
				K,L=models.link_terkait.objects.update_or_create(site__id=E,nama=A.POST.get(_E),defaults={_k:A.POST.get(_k)});M=models.Site.objects.get(id=E);K.site.add(M)
				if L:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(_AB)
		else:B=forms.LinkTerkaitForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		C=get_object_or_404(I)
		if A.method==_K:
			B=forms.LinkTerkaitForm(A.POST,instance=C,label_suffix='')
			if B.is_valid():C.save();N=models.Site.objects.get(id=E);C.site.add(N);messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(_AB)
		else:B=forms.LinkTerkaitForm(instance=C,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif D==_F:C=get_object_or_404(I);C.delete();messages.info(A,mMsgBox.get(_F,C.nama));return redirect(_AB)
	G='link terkait';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_O:F.find_activeMenuList(G),_V:D,_U:B,_R:get_namaOPD(E),_S:O};return render(A,'account/link-terkait.html',P)
@login_required(login_url=_P)
def dokumen(request,mode='',pk=''):
	I='/dashboard/dokumen';D=mode;A=request;cek_user(A);E=get_siteID(A);G=menus.ClsMenus(E,_B);C=_J
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_a)
		K=models.dokumen.objects.filter(site_id=E,id=J)
	if D==_N:
		if A.method==_K:
			C=forms.DokumenForm(A.POST,A.FILES,label_suffix='')
			if C.is_valid():
				M=A.FILES.get(_q)
				if models.dokumen.objects.filter(site_id=E,nama__iexact=A.POST.get(_E)).exists():messages.info(A,mMsgBox.get(_A7,A.POST.get(_E)))
				else:
					B=models.dokumen.objects.create(site_id=E,nama=A.POST.get(_E),admin_id=A.user.id,file_path=M,deskripsi=A.POST.get(_A2),status=A.POST.get(_e));B.size=os.stat(B.file_path.path).st_size;B.save()
					if B:messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)))
					return redirect(I)
		else:C=forms.DokumenForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		F=get_object_or_404(K)
		if A.method==_K:
			C=forms.DokumenForm(A.POST,A.FILES,instance=F,label_suffix='')
			if C.is_valid():
				B=C.save()
				if os.path.isfile(B.file_path.path):B.size=os.stat(B.file_path.path).st_size;B.save()
				messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(I)
		else:C=forms.DokumenForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif D==_F:F=get_object_or_404(K);F.delete();messages.info(A,mMsgBox.get(_F,F.nama));return redirect(I)
	H='dokumen';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_L:G.get_menus(),_Q:G.create_breadCrumb(H),_O:G.find_activeMenuList(H),_V:D,_U:C,_R:get_namaOPD(E),_S:N};return render(A,'account/dokumen.html',O)
@login_required(login_url=_P)
def halaman_statis(request,mode='',pk=''):
	S='/dashboard/halaman-statis';E=mode;A=request;cek_user(A);C=get_siteID(A);N=menus.ClsMenus(C,_B);D=_J;F=_J;O=[]
	if E==_M or E==_F:
		if pk=='':return HttpResponse(_Z)
		V=crypt_uuid4.ClsCryptUuid4();L=V.dec_text(pk)
		if L=='':return HttpResponse(_a)
		T=models.halaman_statis.objects.filter(site_id=C,id=L);H=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=L)
		for B in H:
			if B.photo.jenis!=_s:O.append(B.photo.id)
	elif E==_N:I=formset_factory(forms.PhotoForm,extra=3)
	if E==_N:
		if A.method==_K:
			D=forms.HalamanStatisForm(A.POST);F=I(A.POST)
			if D.is_valid():
				if models.halaman_statis.objects.filter(site_id=C,menu_id=A.POST.get(_L)).count()>1:messages.info(A,mMsgBox.get('menu_already_exists'))
				else:
					G,Z=models.halaman_statis.objects.update_or_create(site_id=C,menu_id=A.POST.get(_L),defaults={_l:C,_G:A.POST.get(_G),_A3:A.POST.get(_A3),'admin_id':A.user.id,'is_edited':_B});B=0
					for W in F:
						J=A.POST.get(_I+str(B)+_c)
						if J:P=A.POST.get(_I+str(B)+_X);Q=save_photo_slideshow(B,C,P,J);G.photo.add(Q);print(_f+str(B))
						B+=1
					messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif E==_M:
		K=get_object_or_404(T);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(O))
		if A.method==_K:
			D=forms.HalamanStatisForm(A.POST,instance=K);F=I(A.POST)
			if D.is_valid():
				G=D.save(commit=_C);G.site_id=C;G.admin_id=A.user.id;G.is_edited=_B;G.save();B=0
				for W in F:
					J=A.POST.get(_I+str(B)+_c)
					if J:P=A.POST.get(_I+str(B)+_X);Q=save_photo_slideshow(B,C,P,J);G.photo.add(Q);print(_f+str(B))
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(instance=K,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=O));messages.info(A,mMsgBox.get(_b))
	elif E==_F:
		for B in H:
			M=models.photo.objects.get(id=B.photo.id)
			if M.file_path:
				if os.path.isfile(M.file_path.path):
					U=Image.open(M.file_path.path)
					if U:U.close()
			M.delete()
		H=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=L)
		if H:H.delete()
		K=get_object_or_404(T);K.delete();messages.info(A,mMsgBox.get(_F,K.judul));return redirect(S)
	R='halaman statis';X=models.menu.objects.filter(nama=R,is_admin_menu=_B);Y={_L:N.get_menus(),_Q:N.create_breadCrumb(R),_O:N.find_activeMenuList(R),_V:E,_U:D,_r:F,_R:get_namaOPD(C),_S:X};return render(A,'account/halaman-statis.html',Y)
@login_required(login_url=_P)
def galery_foto(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-foto';J=photoID;C=mode;A=request;cek_user(A);D=get_siteID(A);L=menus.ClsMenus(D,_B);E=_J;F=_J;J=[];print('mode = ');print(C)
	if C==_M or C==_F:
		if pk=='':return HttpResponse(_Z)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_a)
		R=models.galery_foto.objects.filter(site_id=D,id=M);W=models.galery_foto.objects.filter(site_id=D,id=M)
		for B in W:
			if B.photo.jenis!=_s:J.append(B.photo.id)
	elif C==_N:H=formset_factory(forms.PhotoForm)
	if C==_N:
		if A.method==_K:
			E=forms.GaleryFotoForm(A.POST);F=H(A.POST);B=0
			for X in F:
				G=A.POST.get(_I+str(B)+_c);print(_Ad);print(G)
				if G:N=A.POST.get(_I+str(B)+_X);O=save_photo_slideshow(B,D,N,G);print(_f+str(B));a=models.galery_foto.objects.create(site_id=D,judul=A.POST.get(_G),admin_id=A.user.id,photo_id=O.id)
				B+=1
			return redirect(Q)
		else:E=forms.GaleryFotoForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif C==_M:
		S=get_object_or_404(R);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_K:
			E=forms.GaleryFotoForm(A.POST,instance=S);F=H(A.POST)
			if E.is_valid():
				print('yes form is valid');I=E.save(commit=_C);I.site_id=D;I.admin_id=A.user.id;I.save();B=0
				for X in F:
					G=A.POST.get(_I+str(B)+_c)
					if G:N=A.POST.get(_I+str(B)+_X);O=save_photo_slideshow(B,D,N,G);print(_f+str(B));I.photo_id=O.id;I.save()
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_G)));return redirect(Q)
		else:E=forms.GaleryFotoForm(instance=S,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_b))
	elif C==_F:
		T=''
		for B in R:
			K=models.photo.objects.get(id=B.photo.id);T=B.judul
			if K.file_path:
				if os.path.isfile(K.file_path.path):
					U=Image.open(K.file_path.path)
					if U:U.close()
			K.delete()
		messages.info(A,mMsgBox.get(_F,T));return redirect(Q)
	P='galeri foto';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_L:L.get_menus(),_Q:L.create_breadCrumb(P),_O:L.find_activeMenuList(P),_V:C,_U:E,_r:F,_R:get_namaOPD(D),_S:Y};return render(A,'account/galery-foto.html',Z)
@login_required(login_url=_P)
def popup(request,mode='',pk='',photoID=''):
	X='published';R='/dashboard/popup';J=photoID;D=mode;A=request;cek_user(A);B=get_siteID(A);O=menus.ClsMenus(B,_B);E=_J;F=_J;J=[]
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		Y=crypt_uuid4.ClsCryptUuid4();P=Y.dec_text(pk)
		if P=='':return HttpResponse(_a)
		S=models.popup.objects.filter(site_id=B,id=P);Z=models.popup.objects.filter(site_id=B,id=P)
		for C in Z:
			if C.photo.jenis!=_s:J.append(C.photo.id)
	elif D==_N:H=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_K:
			E=forms.PopupForm(A.POST);F=H(A.POST);C=0
			for a in F:
				I=A.POST.get(_I+str(C)+_c)
				if I:
					K=I.replace(_u,'');L=models.photo.Jenis.POPUP
					if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
					if models.popup.objects.filter(site_id=B,judul__iexact=A.POST.get(_G)).exists():messages.info(A,mMsgBox.get(_A7,A.POST.get(_G)))
					else:M=models.photo.objects.create(site_id=B,jenis=L,file_path=K);G=models.popup.objects.create(site_id=B,judul=A.POST.get(_G),admin_id=A.user.id,status=A.POST.get(_e),photo_id=M.id)
				C+=1
			return redirect(R)
		else:E=forms.PopupForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		T=get_object_or_404(S);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_K:
			E=forms.PopupForm(A.POST,instance=T);F=H(A.POST)
			if E.is_valid():
				if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
				G=E.save(commit=_C);G.site_id=B;G.admin_id=A.user.id;G.save();C=0
				for a in F:
					I=A.POST.get(_I+str(C)+_c)
					if I:
						K=I.replace(_u,'');L=models.photo.Jenis.POPUP;U=A.POST.get(_I+str(C)+_X)
						if U:M,b=models.photo.objects.update_or_create(id=U,defaults={_l:B,_t:L,_q:K})
						else:M,b=models.photo.objects.update_or_create(site_id=B,jenis=L,file_path=K)
						G.photo_id=M.id;G.save()
					C+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_G)));return redirect(R)
		else:E=forms.PopupForm(instance=T,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_b))
	elif D==_F:
		V=''
		for C in S:
			N=models.photo.objects.get(id=C.photo.id);V=C.judul
			if N.file_path:
				if os.path.isfile(N.file_path.path):
					W=Image.open(N.file_path.path)
					if W:W.close()
			N.delete()
		messages.info(A,mMsgBox.get(_F,V));return redirect(R)
	Q='Popup';c=models.menu.objects.filter(nama=Q,is_admin_menu=_B);d={_L:O.get_menus(),_Q:O.create_breadCrumb(Q),_O:O.find_activeMenuList(Q),_V:D,_U:E,_r:F,_R:get_namaOPD(B),_S:c};return render(A,'account/popup.html',d)
@login_required(login_url=_P)
def komentar(request,mode='',pk='',photoID=''):
	B=mode;A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);G=_J;H=_J;photoID=[]
	if B==_F:
		if pk=='':return HttpResponse(_Z)
		I=crypt_uuid4.ClsCryptUuid4();F=I.dec_text(pk)
		if F=='':return HttpResponse(_a)
		J=models.comment.objects.filter(site_id=C,id=F)
	if B==_F:
		for K in J:K.delete()
		return redirect('/dashboard/komentar')
	E='Comment';L=models.menu.objects.filter(nama=E,is_admin_menu=_B);M={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_O:D.find_activeMenuList(E),_V:B,_U:G,_r:H,_R:get_namaOPD(C),_S:L};return render(A,'account/comment.html',M)
@login_required(login_url=_P)
def galery_layanan(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-layanan';J=photoID;D=mode;A=request;cek_user(A);C=get_siteID(A);L=menus.ClsMenus(C,_B);E=_J;F=_J;J=[]
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_a)
		R=models.galery_layanan.objects.filter(site_id=C,id=M);W=models.galery_layanan.objects.filter(site_id=C,id=M)
		for B in W:
			if B.photo.jenis!=_s:J.append(B.photo.id)
	elif D==_N:I=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_K:
			E=forms.GaleryLayananForm(A.POST);F=I(A.POST);B=0
			for X in F:
				G=A.POST.get(_I+str(B)+_c);print('Galery Layanan = ');print(G)
				if G:
					if models.galery_layanan.objects.filter(site_id=C,judul__iexact=A.POST.get(_G)).exists():messages.info(A,mMsgBox.get(_A7,A.POST.get(_G)));print('potential duplicate')
					else:print('else');N=A.POST.get(_I+str(B)+_X);O=save_photo_slideshow(B,C,N,G);print(_f+str(B));H=models.galery_layanan.objects.create(site_id=C,judul=A.POST.get(_G),admin_id=A.user.id,photo_id=O.id);return redirect(Q)
				B+=1
		else:E=forms.GaleryLayananForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		S=get_object_or_404(R);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_K:
			E=forms.GaleryLayananForm(A.POST,instance=S);F=I(A.POST)
			if E.is_valid():
				H=E.save(commit=_C);H.site_id=C;H.admin_id=A.user.id;H.save();B=0
				for X in F:
					G=A.POST.get(_I+str(B)+_c)
					if G:N=A.POST.get(_I+str(B)+_X);O=save_photo_slideshow(B,C,N,G);print(_f+str(B));H.photo_id=O.id;H.save()
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_G)));return redirect(Q)
		else:E=forms.GaleryLayananForm(instance=S,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_b))
	elif D==_F:
		T=''
		for B in R:
			K=models.photo.objects.get(id=B.photo.id);T=B.judul
			if K.file_path:
				if os.path.isfile(K.file_path.path):
					U=Image.open(K.file_path.path)
					if U:U.close()
			K.delete()
		messages.info(A,mMsgBox.get(_F,T));return redirect(Q)
	P='galeri layanan';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_L:L.get_menus(),_Q:L.create_breadCrumb(P),_O:L.find_activeMenuList(P),_V:D,_U:E,_r:F,_R:get_namaOPD(C),_S:Y};return render(A,'account/galery-layanan.html',Z)
@login_required(login_url=_P)
def galery_video(request,mode='',pk='',photoID=''):
	I='/dashboard/galery-video';C=mode;A=request;cek_user(A);D=get_siteID(A);G=menus.ClsMenus(D,_B);B=_J;photoID=[]
	if C==_M or C==_F:
		if pk=='':return HttpResponse(_Z)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_a)
		K=models.galery_video.objects.filter(site_id=D,id=J)
	if C==_N:
		if A.method==_K:
			B=forms.GaleryVideoForm(A.POST)
			if models.galery_video.objects.filter(site_id=D,judul__iexact=A.POST.get(_G)).exists():messages.info(A,mMsgBox.get(_Y,A.POST.get(_G)))
			else:F=models.galery_video.objects.create(site_id=D,judul=A.POST.get(_G),admin_id=A.user.id,embed=A.POST.get('embed'));return redirect(I)
		else:B=forms.GaleryVideoForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_M:
		E=get_object_or_404(K)
		if A.method==_K:
			B=forms.GaleryVideoForm(A.POST,instance=E)
			if B.is_valid():F=B.save(commit=_C);F.site_id=D;F.admin_id=A.user.id;F.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_G)));return redirect(I)
		else:B=forms.GaleryVideoForm(instance=E,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif C==_F:E=get_object_or_404(K);M=E.judul;E.delete();messages.info(A,mMsgBox.get(_F,M));return redirect(I)
	H='galeri video';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_L:G.get_menus(),_Q:G.create_breadCrumb(H),_O:G.find_activeMenuList(H),_V:C,_U:B,_R:get_namaOPD(D),_S:N};return render(A,'account/galery-video.html',O)
@login_required(login_url=_P)
def agenda(request,mode='',pk=''):
	H='/dashboard/agenda';D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);C=_J
	if D==_M or D==_F:
		if pk=='':return HttpResponse(_Z)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_a)
		J=models.agenda.objects.filter(site_id=E,id=I)
	if D==_N:
		if A.method==_K:
			C=forms.AgendaForm(A.POST,label_suffix='')
			if C.is_valid():
				B=C.save(commit=_C);B.site_id=E;B.admin_id=A.user.id
				if A.POST.get(_AQ)!=''and A.POST.get('jam')!='':L=A.POST.get(_AQ)+' '+A.POST.get('jam');B.waktu=datetime.strptime(L,'%d/%m/%Y %H:%M')
				B.save();messages.info(A,mMsgBox.get(_Y,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_M:
		B=get_object_or_404(J)
		if A.method==_K:
			C=forms.AgendaForm(A.POST,A.FILES,instance=B,label_suffix='')
			if C.is_valid():O=C.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(instance=B,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif D==_F:B=get_object_or_404(J);B.delete();messages.info(A,mMsgBox.get(_F,B.nama));return redirect(H)
	G='agenda';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_O:F.find_activeMenuList(G),_V:D,_U:C,_R:get_namaOPD(E),_S:M};return render(A,'account/agenda.html',N)
@login_required(login_url=_P)
def info_hoax(request,mode='',pk=''):
	H='/dashboard/info-hoax';C=mode;A=request;cek_user(A);E=get_siteID(A);print('siteID = ');print(E)
	if not(E==1 or E==68):messages.info(A,_Ae);return redirect(_AD)
	F=menus.ClsMenus(E,_B);B=_J
	if C==_M or C==_F:
		if pk=='':return HttpResponse(_Z)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_a)
		J=models.info_hoax.objects.filter(id=I)
	if C==_N:
		if A.method==_K:
			B=forms.InfoHoaxForm(A.POST,label_suffix='')
			if B.is_valid():
				O,L=models.info_hoax.objects.update_or_create(name=A.POST.get(_m),defaults={_k:A.POST.get(_k)})
				if L:messages.info(A,mMsgBox.get(_Y,A.POST.get(_m)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_m)))
				return redirect(H)
		else:B=forms.InfoHoaxForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_M:
		D=get_object_or_404(J)
		if A.method==_K:
			B=forms.InfoHoaxForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_m)));return redirect(H)
		else:B=forms.InfoHoaxForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_b))
	elif C==_F:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_F,D.name));return redirect(H)
	G='info hoaks';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_O:F.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(E),_S:M};return render(A,'account/info-hoax.html',N)
@login_required(login_url=_P)
def banner_all(request,mode='',pk='',photoID=''):
	T='/dashboard/banner-all';K=photoID;E=mode;A=request;cek_user(A);D=get_siteID(A)
	if not(D==1 or D==68 or D==39 or D==43 or D==69):messages.info(A,_Ae);return redirect(_AD)
	P=menus.ClsMenus(D,_B);C=_J;F=_J;K=[];H=''
	if E==_M or E==_F:
		if pk=='':return HttpResponse(_Z)
		Z=crypt_uuid4.ClsCryptUuid4();H=Z.dec_text(pk)
		if H=='':return HttpResponse(_a)
		U=models.banner_all.objects.filter(id=H);a=models.banner_all.objects.filter(id=H)
		for B in a:
			if B.photo.jenis!=_s:K.append(B.photo.id)
	elif E==_N:I=formset_factory(forms.PhotoForm)
	if E==_N:
		if A.method==_K:
			C=forms.BannerAllForm(A.POST);F=I(A.POST)
			if C.is_valid():
				print('form valid');B=0
				for b in F:
					J=A.POST.get(_I+str(B)+_c)
					if J:
						L=J.replace(_u,'');M=models.photo.Jenis.BANNER_ALL;N=models.photo.objects.create(site_id=D,jenis=M,file_path=L);Q=C.cleaned_data.get('site');G=C.save(commit=_C);G.photo_id=N.id;G.save()
						for R in Q:G.site.add(R)
					B+=1
			return redirect(T)
		else:C=forms.BannerAllForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif E==_M:
		V=get_object_or_404(U);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(K))
		if A.method==_K:
			C=forms.BannerAllForm(A.POST,instance=V);F=I(A.POST)
			if C.is_valid():
				Q=C.cleaned_data.get('site');models.banner_all.site.through.objects.filter(banner_all_id=H).delete();G=C.save();B=0
				for b in F:
					J=A.POST.get(_I+str(B)+_c)
					if J:
						L=J.replace(_u,'');M=models.photo.Jenis.BANNER_ALL;W=A.POST.get(_I+str(B)+_X)
						if W:N,c=models.photo.objects.update_or_create(id=W,defaults={_l:D,_t:M,_q:L})
						else:N,c=models.photo.objects.update_or_create(site_id=D,jenis=M,file_path=L)
						G.photo_id=N.id;G.save()
					B+=1
				for R in Q:G.site.add(R)
				messages.info(A,mMsgBox.get(_T,A.POST.get(_G)));return redirect(T)
		else:C=forms.BannerAllForm(instance=V,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=K));messages.info(A,mMsgBox.get(_b))
	elif E==_F:
		X=''
		for B in U:
			O=models.photo.objects.get(id=B.photo.id);X=B.name
			if O.file_path:
				if os.path.isfile(O.file_path.path):
					Y=Image.open(O.file_path.path)
					if Y:Y.close()
			O.delete()
		messages.info(A,mMsgBox.get(_F,X));return redirect(T)
	S='Banner All';d=models.menu.objects.filter(nama=S,is_admin_menu=_B);e={_L:P.get_menus(),_Q:P.create_breadCrumb(S),_O:P.find_activeMenuList(S),_V:E,_U:C,_r:F,_R:get_namaOPD(D),_S:d};return render(A,'account/banner-all.html',e)
def social_media_ajax(request):
	C=get_siteID(request);A=models.social_media.objects.filter(site_id=C).values(_A,_t,_k,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def instansi_ajax(request):
	C=get_siteID(request);A=models.instansi.objects.filter(site_id=C).values(_A,_E,_AH,'telp',_A8,_AI,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def logo_ajax(request):
	C=get_siteID(request);A=models.logo.objects.filter(site_id=C).values(_A,'position',_v,_D).order_by('-updated_at')
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def banner_ajax(request):
	C=get_siteID(request);A=models.banner.objects.filter(site_id=C).values(_A,'position',_v,_k,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_ajax(request):
	C=get_siteID(request);A=models.menu.objects.filter(site__id=C,is_admin_menu=_C,is_master_menu=_C).values(_A,_E,'href','icon',_w,_D).order_by(_n,_x)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_statis_ajax(request):A=get_siteID(request);B=models.menu.objects.filter(site__id=A,is_statis_menu=_B,is_admin_menu=_C).exclude(href='#').order_by(_n,_x);C=serializers.serialize('json',B,fields=(_A,_E));return HttpResponse(C,content_type='application/json')
def berita_ajax(request):
	C='photo__berita__id';D=get_siteID(request);E={'berita__id':OuterRef(C)};B=models.berita.objects.filter(site_id=D).values(_A,_G,_z,'kategori__nama',_AR,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5);A[_z]=Truncator(A[_z]).words(20)
	F=list(B);return JsonResponse(F,safe=_C)
def kategori_ajax(request):
	C=get_siteID(request);A=models.kategori.objects.filter(site__id=C).values(_A,_E,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def tags_ajax(request):
	C=get_siteID(request);A=models.tags.objects.filter(site__id=C).values(_A,_E,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def pengumuman_ajax(request):
	C='photo__pengumuman__id';D=get_siteID(request);E={'pengumuman__id':OuterRef(C)};B=models.pengumuman.objects.filter(site_id=D).values(_A,_G,_A0,_AR,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5);A[_A0]=Truncator(A[_A0]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def artikel_ajax(request):
	C='photo__artikel__id';D=get_siteID(request);E={'artikel__id':OuterRef(C)};B=models.artikel.objects.filter(site_id=D).values(_A,_G,_A1,_AR,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5);A[_A1]=Truncator(A[_A1]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def dokumen_ajax(request):
	F='extra_field';D='size';B=request;G=get_siteID(B);E=models.dokumen.objects.filter(site_id=G).values(_A,_E,_A2,D,_q,_D)
	for A in E:
		A[_D]=get_natural_datetime(A[_D]);A[D]=naturalsize(A[D]);C=A[_q]
		if'https://'in settings.MEDIA_URL:A[F]='%s%s'%(settings.MEDIA_URL,C)
		else:A[F]='%s://%s%s%s'%(B.scheme,B.get_host(),settings.MEDIA_URL,C)
		A[_q]=Truncator(C).chars(30)
	H=list(E);return JsonResponse(H,safe=_C)
def agenda_ajax(request):
	C=get_siteID(request);B=models.agenda.objects.filter(site_id=C).values(_A,_E,_A2,'lokasi',_AQ,'jam','penyelenggara','dihadiri_oleh',_e,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_A2]=Truncator(A[_A2]).words(30)
	D=list(B);return JsonResponse(D,safe=_C)
def pejabat_ajax(request,pIsDefault):
	C=get_siteID(request);A=models.pejabat.objects.filter(site__id=C,is_default=pIsDefault).values(_A,_E,_AP,_v,_D).order_by(_X)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def link_terkait_ajax(request):
	C=get_siteID(request);A=models.link_terkait.objects.filter(site__id=C).values(_A,_E,_k,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def halaman_statis_ajax(request):
	C='photo__halaman_statis__id';D=get_siteID(request);E={'halaman_statis__id':OuterRef(C)};B=models.halaman_statis.objects.filter(site_id=D).values(_A,_G,_A3,'menu__nama',_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5);A[_A3]=Truncator(A[_A3]).chars(50)
	F=list(B);return JsonResponse(F,safe=_C)
def galery_foto_ajax(request):
	C=get_siteID(request);B=models.galery_foto.objects.filter(site_id=C).values(_A,_G,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def popup_ajax(request):
	C=get_siteID(request);A=models.popup.objects.filter(site_id=C).values(_A,_G,_v,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def komentar_ajax(request):
	C=get_siteID(request);A=models.comment.objects.filter(site_id=C).values(_A,_m,_A8,'body','post__judul',_A4,'active')
	for B in A:B[_A4]=get_natural_datetime(B[_A4])
	D=list(A);return JsonResponse(D,safe=_C)
def galery_layanan_ajax(request):
	C=get_siteID(request);B=models.galery_layanan.objects.filter(site_id=C).values(_A,_G,_e,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def galery_video_ajax(request):
	C=get_siteID(request);B=models.galery_video.objects.filter(site_id=C).values(_A,_G,'embed','embed_video',_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_G]=Truncator(A[_G]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def info_hoax_ajax(request):
	D=get_siteID(request);A=models.info_hoax.objects.all().values(_A,_m,_k,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def banner_all_ajax(request):
	D=get_siteID(request);A=models.banner_all.objects.all().values(_A,_m,_k,_v,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def enc_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.enc_text(data))
def dec_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.dec_text(data))
def toggle_comment_activate(request,pID):A=models.comment.objects.get(id=pID);A.active^=_B;A.save();return HttpResponse('True')
def toggle_comment_activate_all(request):A=models.comment.objects.filter(site_id=get_siteID(request),active=_C).update(active=_B);return HttpResponse('True')
def top_kontributor_berita(request):
	F=models.berita.objects.exclude(admin_id=1).values_list(_AS).annotate(jumlah=Count(_A)).order_by(_AT);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);break
		elif not B and len(A)<6:
			print(_Af)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_j))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_pengumuman(request):
	F=models.pengumuman.objects.exclude(admin_id=1).values_list(_AS).annotate(jumlah=Count(_A)).order_by(_AT);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);break
		elif not B and len(A)<6:
			print(_Af)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_j))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_artikel(request):
	F=models.artikel.objects.exclude(admin_id=1).values_list(_AS).annotate(jumlah=Count(_A)).order_by(_AT);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_j))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_j))+[0]);print('res = ');print(A)
	return JsonResponse(A,safe=_C)
def site_activity(request):
	D=[];G=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	for A in G:
		B=[];H=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for I in H:B.append(I[_A])
		J=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=B);C=len(B);E=J.filter(is_edited=_B).count()
		if C==0:F=0
		else:F=E/C*100
		K={_A:A[_A],_H:A[_H],_AC:C,_o:E,_A5:F};D.append(K)
	return JsonResponse(D,safe=_C)
def site_activity_pie_chart(request):
	C=[];P=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H));Q=0
	for A in P:
		D=[];R=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for S in R:D.append(S[_A])
		T=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=D);E=len(D);H=T.filter(is_edited=_B).count()
		if E==0:F=0
		else:F=H/E*100
		Q+=F;U={_A:A[_A],_H:A[_H],_AC:E,_o:H,_A5:F};C.append(U)
	C=sorted(C,key=lambda x:x[_A5],reverse=_B);B=[];I=10;J=0;K=0;L=0;M=0;G=_C;N=get_siteID(request);O=0
	for A in C:
		J+=1
		if J<I:
			B.append(A)
			if A[_A]==N:G=_B;print(_AU)
		elif len(B)<=I:
			if G:B.append(A);G=_C;print(_AV)
			elif A[_A]==N:B.append(A)
			else:K+=A[_o];L+=A[_AC];M+=A[_A5];O+=1
		else:K+=A[_o];L+=A[_AC];M+=A[_A5];O+=1
	return JsonResponse(B,safe=_C)
def site_activity_detail(request,siteID):
	B=siteID;C=[];H=[];F=list(models.menu.objects.filter(site__id=B,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AM,_x).values(_A,_E,_w))
	for A in F:
		D=models.halaman_statis.objects.filter(site__id=B,menu__id=A[_A],is_edited=_B)[:1]
		if D:
			for G in D:E={_A:A[_A],_n:A[_w],_L:A[_E],_G:G.judul,_o:1}
		else:E={_A:A[_A],_n:A[_w],_L:A[_E],_G:'',_o:0}
		C.append(E)
	return JsonResponse(C,safe=_C)
def site_activity_detail_pie_chart(request,siteID):
	F=siteID;B=[];L=[];I=list(models.menu.objects.filter(site__id=F,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AM,_x).values(_A,_E,_w))
	for A in I:
		G=models.halaman_statis.objects.filter(site__id=F,menu__id=A[_A],is_edited=_B)[:1]
		if G:
			for J in G:H={_A:A[_A],_n:A[_w],_L:A[_E],_G:J.judul,_o:1}
		else:H={_A:A[_A],_n:A[_w],_L:A[_E],_G:'',_o:0}
		B.append(H)
	print('begin create pie chart data');E=len(B);print(E);C=len(list(filter(lambda x:x[_o]==0,B)));print(C);D=len(list(filter(lambda x:x[_o]==1,B)));print(D);C=C/E*100;D=D/E*100;K=[{_m:'Menu Terisi','y':D,'sliced':_B,'selected':_B},{_m:'Menu Kosong','y':C}];return JsonResponse(K,safe=_C)
def site_productivity(request):
	B=[];F=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	for A in F:I=[];C=models.berita.objects.filter(site_id=A[_A]).count();D=models.artikel.objects.filter(site_id=A[_A]).count();E=models.pengumuman.objects.filter(site_id=A[_A]).count();G=C+D+E;H={_A:A[_A],_H:A[_H],_g:C,_h:E,_i:D,_d:G};B.append(H)
	B=sorted(B,key=lambda x:x[_d],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[]
	if J==1:L=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		S=list(models.instansi.objects.filter(kategori_id=J).values(_l))
		for A in S:K.append(A[_l])
		L=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_H).values(_A,_H))
	for A in L:W=[];M=models.berita.objects.filter(site_id=A[_A]).count();N=models.artikel.objects.filter(site_id=A[_A]).count();O=models.pengumuman.objects.filter(site_id=A[_A]).count();T=M+N+O;U={_A:A[_A],_H:A[_H],_g:M,_h:O,_i:N,_d:T};C.append(U)
	C=sorted(C,key=lambda x:x[_d],reverse=_B);B=[];P=10;Q=0;D=0;E=0;F=0;G=0;H=_C;R=get_siteID(request);I=0
	for A in C:
		Q+=1
		if Q<P:
			B.append(A)
			if A[_A]==R:H=_B;print(_AU)
		elif len(B)<=P:
			if H:B.append(A);H=_C;print(_AV)
			elif A[_A]==R:B.append(A)
			else:D+=A[_g];E+=A[_h];F+=A[_i];G+=A[_d];I+=1
		else:D+=A[_g];E+=A[_h];F+=A[_i];G+=A[_d];I+=1
	V={_A:0,_H:_Ag+str(I)+_Ah,_g:D,_h:E,_i:F,_d:G};B.append(V);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_table(request,kategori_id):
	C=kategori_id;B=[];D=[]
	if C==1:E=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		I=list(models.instansi.objects.filter(kategori_id=C).values(_l))
		for A in I:D.append(A[_l])
		E=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_H).values(_A,_H))
	for A in E:L=[];F=models.berita.objects.filter(site_id=A[_A]).count();G=models.artikel.objects.filter(site_id=A[_A]).count();H=models.pengumuman.objects.filter(site_id=A[_A]).count();J=F+G+H;K={_A:A[_A],_H:A[_H],_g:F,_h:H,_i:G,_d:J};B.append(K)
	B=sorted(B,key=lambda x:x[_d],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kualitas_table(request,kategori_id):
	B=kategori_id;C=[];D=[];E=100;J=50
	if B==1:F=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		K=list(models.instansi.objects.filter(kategori_id=B).values(_l))
		for A in K:D.append(A[_l])
		F=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_H).values(_A,_H))
	for A in F:N=[];G=models.berita.objects.filter(site_id=A[_A],word_count__gte=E).count();H=models.artikel.objects.filter(site_id=A[_A],word_count__gte=E).count();I=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=J).count();L=G+H+I;M={_A:A[_A],_H:A[_H],_g:G,_h:I,_i:H,_d:L};C.append(M)
	return JsonResponse(C,safe=_C)
def kontribusi_kualitas_periode(request,kategori_id,periode_id):
	E=kategori_id;F=[];G=[];H=100;L=50
	if E==1:I=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		B=list(models.instansi.objects.filter(kategori_id=E).values(_l))
		for A in B:G.append(A[_l])
		I=list(models.Site.objects.filter(id__in=G).exclude(id=1).order_by(_H).values(_A,_H))
	C=0;D=0;B=periode_id.split('.')
	if len(B)>=2:C=int(B[0]);D=int(B[1])
	if C and D:
		for A in I:Q=[];J=models.berita.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=H).count();print('ret_tmp',J);M=models.artikel.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=H).count();N=models.pengumuman.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=L).count();K=J+M+N;O=K/4*100;P={_A:A[_A],_H:A[_H],_d:K,'persentase':O,'ket':''};F.append(P)
	return JsonResponse(F,safe=_C)
def site_kontribusi_kualitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[];L=100;T=50
	if J==1:M=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		U=list(models.instansi.objects.filter(kategori_id=J).values(_l))
		for A in U:K.append(A[_l])
		M=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_H).values(_A,_H))
	for A in M:Y=[];N=models.berita.objects.filter(site_id=A[_A],word_count__gte=L).count();O=models.artikel.objects.filter(site_id=A[_A],word_count__gte=L).count();P=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=T).count();V=N+O+P;W={_A:A[_A],_H:A[_H],_g:N,_h:P,_i:O,_d:V};C.append(W)
	C=sorted(C,key=lambda x:x[_d],reverse=_B);B=[];Q=10;R=0;D=0;E=0;F=0;G=0;H=_C;S=get_siteID(request);I=0
	for A in C:
		R+=1
		if R<Q:
			B.append(A)
			if A[_A]==S:H=_B;print(_AU)
		elif len(B)<=Q:
			if H:B.append(A);H=_C;print(_AV)
			elif A[_A]==S:B.append(A)
			else:D+=A[_g];E+=A[_h];F+=A[_i];G+=A[_d];I+=1
		else:D+=A[_g];E+=A[_h];F+=A[_i];G+=A[_d];I+=1
	X={_A:0,_H:_Ag+str(I)+_Ah,_g:D,_h:E,_i:F,_d:G};B.append(X);return JsonResponse(B,safe=_C)
def site_ajax(request):
	A=request.GET.get(_AW)
	if A:B=models.Site.objects.filter(domain__icontains=A).exclude(id=1).values(_A,text=F(_H))
	else:B=models.Site.objects.exclude(id=1).values(_A,text=F(_H))
	return JsonResponse({_AX:list(B),_AY:{'more':_B}},safe=_C)
def instansi_kategori_ajax(request):
	A=request.GET.get(_AW)
	if A:B=models.instansi_kategori.objects.filter(nama__icontains=A).values(_A,text=F(_E))
	else:B=models.instansi_kategori.objects.values(_A,text=F(_E))
	return JsonResponse({_AX:list(B),_AY:{'more':_B}},safe=_C)
def post_range(request):
	G='month';E=request.GET.get(_AW);B=[]
	if E:
		C=models.berita.objects.datetimes(_A4,G,tzinfo=timezone.utc)
		for A in C:
			F=A.strftime(_A6)
			if E in F:D={_A:str(A.month)+'.'+str(A.year),_p:F};B.append(D)
	else:
		C=models.berita.objects.datetimes(_A4,G,tzinfo=timezone.utc)
		for A in reversed(C):D={_A:str(A.month)+'.'+str(A.year),_p:A.strftime(_A6)};B.append(D)
	return JsonResponse({_AX:B,_AY:{'more':_B}},safe=_C)
def set_log_all(site_id,is_need_refresh):set_log(site_id,models.OptModelKinds.NEWS,is_need_refresh)
def set_log(site_id,kind,is_need_refresh):
	A=models.Log.objects.filter(site_id=site_id,kind=kind);print('tmp_log',A)
	if A:B=A[0];B.is_need_refresh=is_need_refresh;B.save();print('save complete',B)