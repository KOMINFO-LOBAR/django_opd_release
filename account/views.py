_Ae=' Instansi)'
_Ad='Lainnya ('
_Ac='not found'
_Ab='Menu tidak dapat diakses dari user Anda!'
_Aa='str_foto_path = '
_AZ='form_data_kategori'
_AY='form_data'
_AX='mGrandTotal'
_AW='is_visibled'
_AV='pagination'
_AU='results'
_AT='search'
_AS='mFound = False '
_AR='mFound = True '
_AQ='-jumlah'
_AP='admin'
_AO='tanggal'
_AN='jabatan'
_AM='/dashboard/pejabat'
_AL='parent_id'
_AK='form_img'
_AJ='photo_id'
_AI='photo-str_file_path'
_AH='kode_post'
_AG='alamat'
_AF='siteid'
_AE='mChartNews'
_AD='mChartHit'
_AC='/dashboard/dashboard'
_AB='total_menu'
_AA='/dashboard/link-terkait'
_A9='isi_artikel'
_A8='isi_pengumuman'
_A7='/dashboard/menu'
_A6='photo'
_A5='email'
_A4='%B %Y'
_A3='persen'
_A2='created_at'
_A1='isi_halaman'
_A0='deskripsi'
_z='isi_berita'
_y='order_menu'
_x='potential_duplicate_add'
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
_l='save foto complete '
_k='site_id'
_j='link'
_i='username'
_h='artikel'
_g='pengumuman'
_f='berita'
_e='status'
_d='-id'
_c='total'
_b='-str_file_path'
_a='form_edit'
_Z='Parameter Primary Key tidak ditemukan!'
_Y='Parameter Primary Key tidak tersedia'
_X='save_add'
_W='form_add'
_V='mode'
_U='form'
_T='save_edit'
_S='menu_aktif'
_R='namaOPD'
_Q='breadCrumb'
_P='activeMenuList'
_O='/account/login'
_N='add'
_M='form-'
_L='edit'
_K='menu'
_J='POST'
_I=None
_H='domain'
_G='delete'
_F='judul'
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
from account.commonf import get_topFoto
from account.forms import CustomUserCreationForm
from django_opd.commonf import get_natural_datetime
from opd import menus,models
from.import crypt_uuid4,forms,msgbox
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
mMsgBox=msgbox.ClsMsgBox()
User=get_user_model()
def get_menus(request,siteID,context,active_menu):
	D=context;E=request.user.id;C=User.objects.get(id=E);A=C.groups.all()[:1];
	if A:A=A.get().id
	if not A:
		B=Group.objects.filter(name='Admin')
		if B:B=B.get();A=B.id;C.groups.add(B)
	if A:
		F=menus.Menus(menu_group=A,kinds=2);G=[]
		for H in F.get_menus():
			if H[_AW]:G.append(H)
		D[_K]=G;I=active_menu.replace('_',' ');D[_P]=F.get_active_menu_by_name(I)
	else:pass
def unicode_to_string(value):B='ascii';A=value;A=str(A);A=unicodedata.normalize('NFKD',A).encode(B,'ignore').decode(B);return A
def redirect_to_login(request):
	if request.user.is_authenticated:return redirect(_AC)
	return redirect(_O)
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
	G=request;H=get_siteID(G);L=G.get_host();J=datetime.now();B=ContentType.objects.get(app_label='sites',model='site');B=B.id if B else _I;C=HitCount.objects.filter(content_type_id=B,object_pk=H).first();C=C.id if C else _I;I=[];E={};D='';F=0
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
	B['bulan']=D;B[_f]=H;B[_g]=I;B[_h]=J;return B
def cek_user(request):
	A=request
	if not models.instansi.objects.filter(site_id=get_siteID(A),admin__id=A.user.id).exists():raise Http404("user <b>%s</b> tidak di temukan di domain <b>%s</b>. <a href='%s' onclick='%s'>Logout</a>"%(A.user.username,A.get_host(),'javascript:void(0)','login_again()'))
@login_required(login_url=_O)
def dashboard(request):A=request;cek_user(A);D=get_siteID(A);B=menus.ClsMenus(D,_B);F=get_hit_count(A);G=get_news_count(A);C='analytics';H=models.menu.objects.filter(nama=C,is_admin_menu=_B);E={};E={_K:B.get_menus(),_Q:B.create_breadCrumb(C),_P:B.find_activeMenuList(C),_R:get_namaOPD(D),_S:H,_AD:F,_AE:G};return render(A,'account/dashboard.html',E)
@login_required(login_url=_O)
def dashboard_detail(request):
	B=request;cek_user(B);C=get_siteID(B);E=menus.ClsMenus(C,_B);I=models.berita.objects.exclude(site_id=1).count();J=models.artikel.objects.exclude(site_id=1).count();K=models.pengumuman.objects.exclude(site_id=1).count();G=models.Site.objects.get(id=C);L={_A:G.id,_p:G.domain};D={};A=models.instansi.objects.filter(site_id=C)
	if A:
		A=A.get()
		if A.kategori:D={_A:A.kategori.id,_p:A.kategori.nama}
	if not D:A=models.instansi_kategori.objects.get(id=1);D={_A:A.id,_p:A.nama}
	M=get_hit_count(B);N=get_news_count(B);F='monitoring';O=models.menu.objects.filter(nama=F,is_admin_menu=_B);H={};H={_K:E.get_menus(),_Q:E.create_breadCrumb(F),_P:E.find_activeMenuList(F),_R:get_namaOPD(C),_S:O,_AD:M,_AE:N,_AX:I+K+J,_AF:C,_AY:L,_AZ:D};return render(B,'account/dashboard-detail.html',H)
@login_required(login_url=_O)
def dashboard_content_count(request):
	C=request;cek_user(C);D=get_siteID(C);F=menus.ClsMenus(D,_B);K=models.berita.objects.exclude(site_id=1).count();L=models.artikel.objects.exclude(site_id=1).count();M=models.pengumuman.objects.exclude(site_id=1).count();H=models.Site.objects.get(id=D);N={_A:H.id,_p:H.domain};B=datetime.now();I={_A:f"{B.month}.{B.year}",_p:B.strftime(_A4)};E={};A=models.instansi.objects.filter(site_id=D)
	if A:
		A=A.get()
		if A.kategori:E={_A:A.kategori.id,_p:A.kategori.nama}
	if not E:A=models.instansi_kategori.objects.get(id=1);E={_A:A.id,_p:A.nama}
	O=get_hit_count(C);P=get_news_count(C);G='content count';Q=models.menu.objects.filter(nama=G,is_admin_menu=_B);J={};J={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_P:F.find_activeMenuList(G),_R:get_namaOPD(D),_S:Q,_AD:O,_AE:P,_AX:K+M+L,_AF:D,_AY:N,'form_data_month':I,_AZ:E};return render(C,'account/dashboard-content-count.html',J)
def register(request):
	A=request
	if A.method==_J:
		B=CustomUserCreationForm(A.POST)
		if B.is_valid():C=B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_i)));return redirect(_O)
	else:B=forms.CustomUserCreationForm(label_suffix='')
	return render(A,'account/register.html',{_U:B})
@login_required(login_url=_O)
def social_media(request,mode='',pk=''):
	H='/dashboard/social-media';C=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_I
	if C==_L or C==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.social_media.objects.filter(site_id=E,id=I)
	if C==_N:
		if A.method==_J:
			B=forms.SocialMediaForm(A.POST,label_suffix='')
			if B.is_valid():
				if models.social_media.objects.filter(site_id=E,link=A.POST.get(_j)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_j)))
				else:
					L=models.social_media.objects.create(site_id=E,jenis=A.POST.get(_t),link=A.POST.get(_j))
					if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_t)))
					return redirect(H)
		else:B=forms.SocialMediaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_L:
		D=get_object_or_404(J)
		if A.method==_J:
			B=forms.SocialMediaForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_t)));return redirect(H)
		else:B=forms.SocialMediaForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.jenis));return redirect(H)
	G='social media';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_P:F.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(E),_S:M};return render(A,'account/social-media.html',N)
@login_required(login_url=_O)
def instansi(request,mode='',pk=''):
	I='/dashboard/instansi';C=mode;A=request;cek_user(A);D=get_siteID(A);E=menus.ClsMenus(D,_B);B=_I
	if C==_L:
		if pk=='':return HttpResponse(_Y)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		K=models.instansi.objects.filter(site_id=D,id=H)
	if C==_N:
		if A.method==_J:
			B=forms.InstansiForm(A.POST,label_suffix='')
			if B.is_valid():
				L=models.User.objects.get(id=A.user.id);M,N=models.instansi.objects.update_or_create(site_id=D,defaults={_E:A.POST.get(_E),_AG:A.POST.get(_AG),'telp':A.POST.get('telp'),_A5:A.POST.get(_A5),_AH:A.POST.get(_AH)});M.admin.add(L)
				if N:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(I)
		else:B=forms.InstansiForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_L:
		F=get_object_or_404(K)
		if A.method==_J:
			B=forms.InstansiForm(A.POST,instance=F,label_suffix='')
			if B.is_valid():F.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(I)
		else:B=forms.InstansiForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	G='instansi';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:E.get_menus(),_Q:E.create_breadCrumb(G),_P:E.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(D),_S:O};return render(A,'account/instansi.html',P)
@login_required(login_url=_O)
def logo(request,mode='',pk=''):
	K='logo';J='Logo ';C='logo-position';A=request;cek_user(A);B=get_siteID(A);D=menus.ClsMenus(B,_B);E=_I;F=_I
	if mode==_N:
		if A.method==_J:
			E=forms.LogoForm(A.POST);F=forms.PhotoForm(A.POST)
			if A.POST.get(C).upper()=='TOP':H=models.photo.Jenis.LOGO_TOP
			else:H=models.photo.Jenis.LOGO_BOTTOM
			I=A.POST.get(_AI)
			if I:
				L=I.replace(_u,'');M,N=models.photo.objects.update_or_create(site_id=B,jenis=H,defaults={_q:L});Q,R=models.logo.objects.update_or_create(site_id=B,position=A.POST.get(C),defaults={_AJ:M.id})
				if N:messages.info(A,mMsgBox.get(_X,J+A.POST.get(C)))
				else:messages.info(A,mMsgBox.get(_T,J+A.POST.get(C)))
			return redirect('/dashboard/logo')
		else:E=forms.LogoForm(label_suffix='',prefix=K);F=forms.PhotoForm(label_suffix='',prefix=_A6);messages.info(A,mMsgBox.get(_W))
	G=K;O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:D.get_menus(),_Q:D.create_breadCrumb(G),_P:D.find_activeMenuList(G),_V:mode,_U:E,_AK:F,_R:get_namaOPD(B),_S:O};return render(A,'account/logo.html',P)
@login_required(login_url=_O)
def banner(request,mode='',pk=''):
	J='banner';A=request;cek_user(A);C=get_siteID(A);E=menus.ClsMenus(C,_B);F=_I;G=_I
	if mode==_N:
		if A.method==_J:
			F=forms.BannerForm(A.POST);G=forms.PhotoForm(A.POST);B=A.POST.get('banner-str_banner_position')
			if B=='bottom':D=models.photo.Jenis.BANNER_BOTTOM
			elif B=='middle1':D=models.photo.Jenis.BANNER_MIDDLE1
			elif B=='middle2':D=models.photo.Jenis.BANNER_MIDDLE2
			else:D=models.photo.Jenis.BANNER_TOP
			H=A.POST.get(_AI);
			if H:
				K=H.replace(_u,'');L,M=models.photo.objects.update_or_create(site_id=C,jenis=D,defaults={_q:K});P,Q=models.banner.objects.update_or_create(site_id=C,position=B,defaults={_AJ:L.id,_j:A.POST.get('banner-link')})
				if M:messages.info(A,mMsgBox.get(_X,B))
				else:messages.info(A,mMsgBox.get(_T,B))
			return redirect('/dashboard/banner')
		else:F=forms.BannerForm(label_suffix='',prefix=J);G=forms.PhotoForm(label_suffix='',prefix=_A6);messages.info(A,mMsgBox.get(_W))
	I=J;N=models.menu.objects.filter(nama=I,is_admin_menu=_B);O={_K:E.get_menus(),_Q:E.create_breadCrumb(I),_P:E.find_activeMenuList(I),_V:mode,_U:F,_AK:G,_R:get_namaOPD(C),_S:N};return render(A,'account/banner.html',O)
def menu_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.menu.objects.filter(is_master_menu=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('menu_refresh'));return redirect(_A7)
def menu_update_visibled(request,pk,is_visible):
	A=models.Site.objects.get(id=get_siteID(request));B=models.menu.objects.get(id=pk)
	if is_visible:B.site.add(A)
	else:B.site.remove(A)
	return HttpResponse('True')
def menu_is_have_child(menu_id):return models.menu.objects.filter(parent__id=menu_id).exists()
@login_required(login_url=_O)
def menu(request,mode='',pk=''):
	U='delete_fail';T='master_menu';S='is_master_menu';D=mode;A=request;cek_user(A);E=get_siteID(A);J=menus.ClsMenus(E,_B);C=_I;L=_I;F=_I
	if D=='':V=menus.ClsMenus(E,_C,_B);L=V.get_menus()
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();M=W.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		N=models.menu.objects.filter(site__id=E,id=M)
	if D==_N or D==_n:
		if D==_n:F=pk
		if A.method==_J:
			C=forms.MenuForm(A.POST,label_suffix='')
			if C.is_valid():
				G=models.Site.objects.get(id=E);F=A.POST.get(_n)
				if not F:F=_I
				O=_B;P=models.menu.objects.filter(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F).values_list(S,flat=_B)
				if P.count()>0:
					if P[0]==_B:messages.info(A,mMsgBox.get(T));C=forms.MenuForm(label_suffix='');O=_C
				if O:
					X,Y=models.menu.objects.update_or_create(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F,defaults={_E:A.POST.get(_E),'href':'menu/'+slugify(A.POST.get(_E)),'icon':A.POST.get('icon'),_y:A.POST.get(_y),_AW:_B,'is_statis_menu':_B});X.site.add(G)
					if Y:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
					return redirect(_A7)
		else:C=forms.MenuForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		B=get_object_or_404(N)
		if A.method==_J:
			C=forms.MenuForm(A.POST,instance=B,label_suffix='')
			if A.POST.get(_n)==str(B.id):messages.info(A,mMsgBox.get('circular_menu'));C=forms.MenuForm(instance=B,label_suffix='')
			elif A.POST.get(S):messages.info(A,mMsgBox.get(T));C=forms.MenuForm(instance=B,label_suffix='')
			elif C.is_valid():B=C.save(commit=_C);B.is_statis_menu=1;B.is_visibled=1;B.save();G=models.Site.objects.get(id=E);B.site.add(G);messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(_A7)
		else:C=forms.MenuForm(instance=B,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:
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
			messages.info(A,mMsgBox.get(_G,B.nama))
		return redirect(_A7)
	K=_K;b=models.menu.objects.filter(nama=K,is_admin_menu=_B);c={_K:J.get_menus(),_Q:J.create_breadCrumb(K),_P:J.find_activeMenuList(K),_V:D,_U:C,'menu_master':L,_AL:F,_R:get_namaOPD(E),_S:b};return render(A,'account/menu.html',c)
def delete_photo(request):
	C=range(3)
	for B in C:
		A=request.POST.get('file_path_'+str(B));
		if A!='':
			if os.path.isfile(A):os.remove(A);
	return HttpResponse('OKE')
def upload_photo(request,width,height):
	O='JPEG';N='RGBA';M='image/png';J='/';I='.jpg';G=request;A=G.FILES.get(_A6);H=G.POST.get('old_photo')
	if H:
		if os.path.isfile(H):os.remove(H);
	P=get_siteID(G);Q=Image.open(io.BytesIO(A.read()));B=Q.resize((width,height),Image.ANTIALIAS);F=datetime.now();R=str(P)+'-'+F.strftime('%Y%m%d-%H%M%S-%f');S=F.strftime('%Y');T=F.strftime('%m');U=F.strftime('%d')
	if A.content_type=='image/gif':C='.gif'
	elif A.content_type=='image/jpeg':C=I
	elif A.content_type=='image/jpg':C=I
	elif A.content_type==M:C=I
	elif A.content_type=='image/bmp':C='.bmp'
	else:C='.ief'
	V=settings.BASE_DIR;K=settings.MEDIA_ROOT;D='crop/'+S+J+T+J+U+J;E=os.path.join(K,D);W=os.makedirs(E,exist_ok=_B);D=D+R+C;E=os.path.join(K,D)
	if A.content_type==M:
		B.load();L=Image.new('RGB',B.size,(255,255,255))
		if B.mode==N:L.paste(B,mask=B.getchannel('A'));L.save(E,O,quality=80,optimize=_B)
		else:B.save(E,O,quality=80,optimize=_B)
	else:B.save(E,quality=80,optimize=_B)
	return HttpResponse(D)
def get_photo_kind(idx):
	B=idx;A=_I
	if B==0:A=models.photo.Jenis.HIGHLIGHT1
	elif B==1:A=models.photo.Jenis.HIGHLIGHT2
	elif B==2:A=models.photo.Jenis.HIGHLIGHT3
	return A
def save_photo_slideshow(idx,site_id,photo_id,str_foto_path):
	C=photo_id;B=site_id;D=get_photo_kind(idx);E=str_foto_path;
	if C:A=models.photo.objects.get(id=C);A.site_id=B;A.jenis=D;A.file_path=E;A.save();
	else:A=models.photo.objects.create(site_id=B,jenis=D,file_path=E);
	return A
def save_tags(tag_list,obj_master):
	C=obj_master;B=tag_list;D=models.berita.tags.through.objects.filter(berita_id=C.id)
	if D:D.delete()
	A=0
	while A<len(B):E=models.tags.objects.get(id=B[A]);C.tags.add(E);A+=1
@login_required(login_url=_O)
def berita(request,mode='',pk='',photoID=''):
	W='/dashboard/berita';O=photoID;G=mode;A=request;cek_user(A);F=get_siteID(A);R=menus.ClsMenus(F,_B);D=_I;H=_I;O=[]
	if G==_L or G==_G:
		if pk=='':return HttpResponse(_Y)
		a=crypt_uuid4.ClsCryptUuid4();P=a.dec_text(pk)
		if P=='':return HttpResponse(_Z)
		X=models.berita.objects.filter(site_id=F,id=P);J=models.berita.photo.through.objects.filter(berita__site=F,berita__id=P)
		for B in J:
			if B.photo.jenis!=_s:O.append(B.photo.id)
	elif G==_N:K=formset_factory(forms.PhotoForm,extra=3)
	if G==_N:
		if A.method==_J:
			D=forms.BeritaForm(A.POST);H=K(A.POST)
			if D.is_valid():
				C=A.POST.get(_F);E=A.POST.get(_z)
				if not C.isascii():C=unicode_to_string(C)
				if not E.isascii():E=unicode_to_string(E)
				S=models.berita.objects.create(site_id=F,judul=C,admin_id=A.user.id,kategori_id=A.POST.get('kategori'),isi_berita=E,status=A.POST.get(_e));T=A.POST.getlist('tags');save_tags(T,S);B=0
				for b in H:
					L=A.POST.get(_M+str(B)+_b)
					if L:
						U=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,F,U,L)
						if Q:S.photo.add(Q);
					B+=1
				if S:messages.info(A,mMsgBox.get(_X,C))
				return redirect(W)
		else:D=forms.BeritaForm(label_suffix='');H=K();messages.info(A,mMsgBox.get(_W))
	elif G==_L:
		M=get_object_or_404(X);K=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(O))
		if A.method==_J:
			D=forms.BeritaForm(A.POST,instance=M);H=K(A.POST)
			if D.is_valid():
				E=D.cleaned_data.get(_z)
				if not E.isascii():E=unicode_to_string(E)
				C=D.cleaned_data.get(_F)
				if not C.isascii():C=unicode_to_string(C)
				I=D.save(commit=_C);I.judul=C;I.isi_berita=E;I.site_id=F;I.admin_id=A.user.id;I.save();T=A.POST.getlist('tags');save_tags(T,I);B=0
				for b in H:
					L=A.POST.get(_M+str(B)+_b)
					if L!='':U=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,F,U,L);I.photo.add(Q);
					B+=1
				messages.info(A,mMsgBox.get(_T,C));return redirect(W)
		else:D=forms.BeritaForm(instance=M,label_suffix='');H=K(queryset=models.photo.objects.filter(id__in=O));messages.info(A,mMsgBox.get(_a))
	elif G==_G:
		for B in J:
			N=models.photo.objects.get(id=B.photo.id)
			if N.file_path:
				if os.path.exists(N.file_path.path):
					Y=Image.open(N.file_path.path)
					if Y:Y.close()
			N.delete()
		J=models.berita.photo.through.objects.filter(berita__site=F,berita__id=P)
		if J:J.delete()
		M=get_object_or_404(X);M.delete();messages.info(A,mMsgBox.get(_G,M.judul));return redirect(W)
	V=_f;c=models.menu.objects.filter(nama=V,is_admin_menu=_B);Z={};Z={_K:R.get_menus(),_Q:R.create_breadCrumb(V),_P:R.find_activeMenuList(V),_V:G,_U:D,_r:H,_R:get_namaOPD(F),_S:c};return render(A,'account/berita.html',Z)
@login_required(login_url=_O)
def kategori(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_I
	if mode==_N:
		if A.method==_J:
			B=forms.KategoriForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.kategori.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect('/dashboard/kategori')
		else:B=forms.KategoriForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='kategori';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_P:D.find_activeMenuList(E),_V:mode,_U:B,_R:get_namaOPD(C),_S:I};return render(A,'account/kategori.html',J)
@login_required(login_url=_O)
def tags(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_I
	if mode==_N:
		if A.method==_J:
			B=forms.TagsForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.tags.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect('/dashboard/tags')
		else:B=forms.TagsForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='tags';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_P:D.find_activeMenuList(E),_V:mode,_U:B,_R:get_namaOPD(C),_S:I};return render(A,'account/tags.html',J)
@login_required(login_url=_O)
def pengumuman(request,mode='',pk=''):
	W='Pengumuman';S='/dashboard/pengumuman';D=mode;A=request;cek_user(A);C=get_siteID(A);N=menus.ClsMenus(C,_B);E=_I;F=_I;O=[]
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		X=crypt_uuid4.ClsCryptUuid4();K=X.dec_text(pk)
		if K=='':return HttpResponse(_Z)
		T=models.pengumuman.objects.filter(site_id=C,id=K);G=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=K)
		for B in G:
			if B.photo.jenis!=_s:O.append(B.photo.id)
	elif D==_N:H=formset_factory(forms.PhotoForm,extra=3)
	if D==_N:
		if A.method==_J:
			E=forms.PengumumanForm(A.POST);F=H(A.POST)
			if models.pengumuman.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_F)))
			else:
				U=models.pengumuman.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_pengumuman=A.POST.get(_A8),status=A.POST.get(_e));B=0
				for Y in F:
					I=A.POST.get(_M+str(B)+_b)
					if I:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,I);U.photo.add(Q);
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,W))
				return redirect(S)
		else:E=forms.PengumumanForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		J=get_object_or_404(T);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(O))
		if A.method==_J:
			E=forms.PengumumanForm(A.POST,instance=J);F=H(A.POST)
			if E.is_valid():
				L=E.save(commit=_C);L.site_id=C;L.admin_id=A.user.id;L.save();B=0
				for Y in F:
					I=A.POST.get(_M+str(B)+_b)
					if I:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,I);L.photo.add(Q);
					B+=1
			messages.info(A,mMsgBox.get(_T,W));return redirect(S)
		else:E=forms.PengumumanForm(instance=J,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=O));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		for B in G:
			M=models.photo.objects.get(id=B.photo.id)
			if M.file_path:
				if os.path.isfile(M.file_path.path):
					V=Image.open(M.file_path.path)
					if V:V.close()
			M.delete()
		G=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=K)
		if G:G.delete()
		J=get_object_or_404(T);J.delete();messages.info(A,mMsgBox.get(_G,J.judul));return redirect(S)
	R=_g;Z=models.menu.objects.filter(nama=R,is_admin_menu=_B);a={_K:N.get_menus(),_Q:N.create_breadCrumb(R),_P:N.find_activeMenuList(R),_V:D,_U:E,_r:F,_R:get_namaOPD(C),_S:Z};return render(A,'account/pengumuman.html',a)
@login_required(login_url=_O)
def artikel(request,mode='',pk=''):
	S='/dashboard/artikel';D=mode;A=request;cek_user(A);C=get_siteID(A);N=menus.ClsMenus(C,_B);E=_I;F=_I;O=[]
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();K=W.dec_text(pk)
		if K=='':return HttpResponse(_Z)
		T=models.artikel.objects.filter(site_id=C,id=K);G=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=K)
		for B in G:
			if B.photo.jenis!=_s:O.append(B.photo.id)
	elif D==_N:H=formset_factory(forms.PhotoForm,extra=3)
	if D==_N:
		if A.method==_J:
			E=forms.ArtikelForm(A.POST);F=H(A.POST)
			if models.artikel.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_F)))
			else:
				U=models.artikel.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_artikel=A.POST.get(_A9),status=A.POST.get(_e));B=0
				for X in F:
					I=A.POST.get(_M+str(B)+_b)
					if I:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,I);U.photo.add(Q);
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
				return redirect(S)
		else:E=forms.ArtikelForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		J=get_object_or_404(T);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(O))
		if A.method==_J:
			E=forms.ArtikelForm(A.POST,instance=J);F=H(A.POST)
			if E.is_valid():
				L=E.save(commit=_C);L.site_id=C;L.admin_id=A.user.id;L.save();B=0
				for X in F:
					I=A.POST.get(_M+str(B)+_b)
					if I:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,I);L.photo.add(Q);
					B+=1
			messages.info(A,mMsgBox.get(_T,'Artikel'));return redirect(S)
		else:E=forms.ArtikelForm(instance=J,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=O));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		for B in G:
			M=models.photo.objects.get(id=B.photo.id)
			if M.file_path:
				if os.path.isfile(M.file_path.path):
					V=Image.open(M.file_path.path)
					if V:V.close()
			M.delete()
		G=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=K)
		if G:G.delete()
		J=get_object_or_404(T);J.delete();messages.info(A,mMsgBox.get(_G,J.judul));return redirect(S)
	R=_h;Y=models.menu.objects.filter(nama=R,is_admin_menu=_B);Z={_K:N.get_menus(),_Q:N.create_breadCrumb(R),_P:N.find_activeMenuList(R),_V:D,_U:E,_r:F,_R:get_namaOPD(C),_S:Y};return render(A,'account/artikel.html',Z)
def pejabat_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.pejabat.objects.filter(is_default=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('pejabat_refresh'));return redirect(_AM)
@login_required(login_url=_O)
def pejabat(request,mode='',pk=''):
	C=mode;A=request;cek_user(A);B=get_siteID(A);F=menus.ClsMenus(B,_B);D=_I;G=_I
	if C==_L or C==_G:
		if pk=='':return HttpResponse(_Y)
		M=crypt_uuid4.ClsCryptUuid4();J=M.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		N=models.pejabat.objects.filter(site__id=B,id=J)
	if C==_N:
		if A.method==_J:
			D=forms.PejabatForm(A.POST);G=forms.PhotoForm(A.POST);O=models.photo.Jenis.PEJABAT_OPD
			if D.is_valid():
				K=A.POST.get(_AI)
				if K:
					P=K.replace(_u,'');Q,R=models.photo.objects.update_or_create(site_id=B,jenis=O,defaults={_q:P});L,S=models.pejabat.objects.update_or_create(site__id=B,jabatan_index=models.pejabat.Position.PEJABAT_OPD,defaults={_AJ:Q.id,_E:A.POST.get(_E),_AN:A.POST.get(_AN),'admin_id':A.user.id,'is_default':0});T=models.Site.objects.get(id=B);L.site.add(T)
					if R:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(_AM)
		else:D=forms.PejabatForm(label_suffix='');G=forms.PhotoForm(label_suffix='',prefix=_A6);messages.info(A,mMsgBox.get(_W))
	elif C==_G:
		E=get_object_or_404(N);H=models.photo.objects.filter(id=E.photo.id);
		if H:H.delete()
		E.delete();messages.info(A,mMsgBox.get(_G,E.nama));return redirect(_AM)
	I='pejabat';U=models.menu.objects.filter(nama=I,is_admin_menu=_B);V={_K:F.get_menus(),_Q:F.create_breadCrumb(I),_P:F.find_activeMenuList(I),_V:C,_U:D,_AK:G,_R:get_namaOPD(B),_S:U};return render(A,'account/pejabat.html',V)
def link_terkait_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.link_terkait.objects.all()
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('link_terkait_refresh'));return redirect(_AA)
@login_required(login_url=_O)
def link_terkait(request,mode='',pk=''):
	D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_I
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		I=models.link_terkait.objects.filter(site__id=E,id=H)
	if D==_N:
		if A.method==_J:
			B=forms.LinkTerkaitForm(A.POST,label_suffix='')
			if B.is_valid():
				K,L=models.link_terkait.objects.update_or_create(site__id=E,nama=A.POST.get(_E),defaults={_j:A.POST.get(_j)});M=models.Site.objects.get(id=E);K.site.add(M)
				if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_E)))
				return redirect(_AA)
		else:B=forms.LinkTerkaitForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		C=get_object_or_404(I)
		if A.method==_J:
			B=forms.LinkTerkaitForm(A.POST,instance=C,label_suffix='')
			if B.is_valid():C.save();N=models.Site.objects.get(id=E);C.site.add(N);messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(_AA)
		else:B=forms.LinkTerkaitForm(instance=C,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:C=get_object_or_404(I);C.delete();messages.info(A,mMsgBox.get(_G,C.nama));return redirect(_AA)
	G='link terkait';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_P:F.find_activeMenuList(G),_V:D,_U:B,_R:get_namaOPD(E),_S:O};return render(A,'account/link-terkait.html',P)
@login_required(login_url=_O)
def dokumen(request,mode='',pk=''):
	I='/dashboard/dokumen';D=mode;A=request;cek_user(A);E=get_siteID(A);G=menus.ClsMenus(E,_B);C=_I
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		K=models.dokumen.objects.filter(site_id=E,id=J)
	if D==_N:
		if A.method==_J:
			C=forms.DokumenForm(A.POST,A.FILES,label_suffix='')
			if C.is_valid():
				M=A.FILES.get(_q)
				if models.dokumen.objects.filter(site_id=E,nama__iexact=A.POST.get(_E)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_E)))
				else:
					B=models.dokumen.objects.create(site_id=E,nama=A.POST.get(_E),admin_id=A.user.id,file_path=M,deskripsi=A.POST.get(_A0),status=A.POST.get(_e));B.size=os.stat(B.file_path.path).st_size;B.save()
					if B:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					return redirect(I)
		else:C=forms.DokumenForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		F=get_object_or_404(K)
		if A.method==_J:
			C=forms.DokumenForm(A.POST,A.FILES,instance=F,label_suffix='')
			if C.is_valid():
				B=C.save()
				if os.path.isfile(B.file_path.path):B.size=os.stat(B.file_path.path).st_size;B.save()
				messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(I)
		else:C=forms.DokumenForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:F=get_object_or_404(K);F.delete();messages.info(A,mMsgBox.get(_G,F.nama));return redirect(I)
	H='dokumen';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_K:G.get_menus(),_Q:G.create_breadCrumb(H),_P:G.find_activeMenuList(H),_V:D,_U:C,_R:get_namaOPD(E),_S:N};return render(A,'account/dokumen.html',O)
@login_required(login_url=_O)
def halaman_statis(request,mode='',pk=''):
	S='/dashboard/halaman-statis';E=mode;A=request;cek_user(A);C=get_siteID(A);N=menus.ClsMenus(C,_B);D=_I;F=_I;O=[]
	if E==_L or E==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();L=V.dec_text(pk)
		if L=='':return HttpResponse(_Z)
		T=models.halaman_statis.objects.filter(site_id=C,id=L);H=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=L)
		for B in H:
			if B.photo.jenis!=_s:O.append(B.photo.id)
	elif E==_N:I=formset_factory(forms.PhotoForm,extra=3)
	if E==_N:
		if A.method==_J:
			D=forms.HalamanStatisForm(A.POST);F=I(A.POST)
			if D.is_valid():
				if models.halaman_statis.objects.filter(site_id=C,menu_id=A.POST.get(_K)).count()>1:messages.info(A,mMsgBox.get('menu_already_exists'))
				else:
					G,Z=models.halaman_statis.objects.update_or_create(site_id=C,menu_id=A.POST.get(_K),defaults={_k:C,_F:A.POST.get(_F),_A1:A.POST.get(_A1),'admin_id':A.user.id,'is_edited':_B});B=0
					for W in F:
						J=A.POST.get(_M+str(B)+_b)
						if J:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,J);G.photo.add(Q);
						B+=1
					messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif E==_L:
		K=get_object_or_404(T);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(O))
		if A.method==_J:
			D=forms.HalamanStatisForm(A.POST,instance=K);F=I(A.POST)
			if D.is_valid():
				G=D.save(commit=_C);G.site_id=C;G.admin_id=A.user.id;G.is_edited=_B;G.save();B=0
				for W in F:
					J=A.POST.get(_M+str(B)+_b)
					if J:P=A.POST.get(_M+str(B)+_d);Q=save_photo_slideshow(B,C,P,J);G.photo.add(Q);
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(instance=K,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=O));messages.info(A,mMsgBox.get(_a))
	elif E==_G:
		for B in H:
			M=models.photo.objects.get(id=B.photo.id)
			if M.file_path:
				if os.path.isfile(M.file_path.path):
					U=Image.open(M.file_path.path)
					if U:U.close()
			M.delete()
		H=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=L)
		if H:H.delete()
		K=get_object_or_404(T);K.delete();messages.info(A,mMsgBox.get(_G,K.judul));return redirect(S)
	R='halaman statis';X=models.menu.objects.filter(nama=R,is_admin_menu=_B);Y={_K:N.get_menus(),_Q:N.create_breadCrumb(R),_P:N.find_activeMenuList(R),_V:E,_U:D,_r:F,_R:get_namaOPD(C),_S:X};return render(A,'account/halaman-statis.html',Y)
@login_required(login_url=_O)
def galery_foto(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-foto';J=photoID;C=mode;A=request;cek_user(A);D=get_siteID(A);L=menus.ClsMenus(D,_B);E=_I;F=_I;J=[];
	if C==_L or C==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_foto.objects.filter(site_id=D,id=M);W=models.galery_foto.objects.filter(site_id=D,id=M)
		for B in W:
			if B.photo.jenis!=_s:J.append(B.photo.id)
	elif C==_N:H=formset_factory(forms.PhotoForm)
	if C==_N:
		if A.method==_J:
			E=forms.GaleryFotoForm(A.POST);F=H(A.POST);B=0
			for X in F:
				G=A.POST.get(_M+str(B)+_b);
				if G:N=A.POST.get(_M+str(B)+_d);O=save_photo_slideshow(B,D,N,G);a=models.galery_foto.objects.create(site_id=D,judul=A.POST.get(_F),admin_id=A.user.id,photo_id=O.id)
				B+=1
			return redirect(Q)
		else:E=forms.GaleryFotoForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif C==_L:
		S=get_object_or_404(R);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.GaleryFotoForm(A.POST,instance=S);F=H(A.POST)
			if E.is_valid():
				I=E.save(commit=_C);I.site_id=D;I.admin_id=A.user.id;I.save();B=0
				for X in F:
					G=A.POST.get(_M+str(B)+_b)
					if G:N=A.POST.get(_M+str(B)+_d);O=save_photo_slideshow(B,D,N,G);I.photo_id=O.id;I.save()
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_F)));return redirect(Q)
		else:E=forms.GaleryFotoForm(instance=S,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_a))
	elif C==_G:
		T=''
		for B in R:
			K=models.photo.objects.get(id=B.photo.id);T=B.judul
			if K.file_path:
				if os.path.isfile(K.file_path.path):
					U=Image.open(K.file_path.path)
					if U:U.close()
			K.delete()
		messages.info(A,mMsgBox.get(_G,T));return redirect(Q)
	P='galeri foto';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_K:L.get_menus(),_Q:L.create_breadCrumb(P),_P:L.find_activeMenuList(P),_V:C,_U:E,_r:F,_R:get_namaOPD(D),_S:Y};return render(A,'account/galery-foto.html',Z)
@login_required(login_url=_O)
def popup(request,mode='',pk='',photoID=''):
	X='published';R='/dashboard/popup';J=photoID;D=mode;A=request;cek_user(A);B=get_siteID(A);O=menus.ClsMenus(B,_B);E=_I;F=_I;J=[]
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		Y=crypt_uuid4.ClsCryptUuid4();P=Y.dec_text(pk)
		if P=='':return HttpResponse(_Z)
		S=models.popup.objects.filter(site_id=B,id=P);Z=models.popup.objects.filter(site_id=B,id=P)
		for C in Z:
			if C.photo.jenis!=_s:J.append(C.photo.id)
	elif D==_N:H=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			E=forms.PopupForm(A.POST);F=H(A.POST);C=0
			for a in F:
				I=A.POST.get(_M+str(C)+_b)
				if I:
					K=I.replace(_u,'');L=models.photo.Jenis.POPUP
					if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
					if models.popup.objects.filter(site_id=B,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_F)))
					else:M=models.photo.objects.create(site_id=B,jenis=L,file_path=K);G=models.popup.objects.create(site_id=B,judul=A.POST.get(_F),admin_id=A.user.id,status=A.POST.get(_e),photo_id=M.id)
				C+=1
			return redirect(R)
		else:E=forms.PopupForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		T=get_object_or_404(S);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.PopupForm(A.POST,instance=T);F=H(A.POST)
			if E.is_valid():
				if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
				G=E.save(commit=_C);G.site_id=B;G.admin_id=A.user.id;G.save();C=0
				for a in F:
					I=A.POST.get(_M+str(C)+_b)
					if I:
						K=I.replace(_u,'');L=models.photo.Jenis.POPUP;U=A.POST.get(_M+str(C)+_d)
						if U:M,b=models.photo.objects.update_or_create(id=U,defaults={_k:B,_t:L,_q:K})
						else:M,b=models.photo.objects.update_or_create(site_id=B,jenis=L,file_path=K)
						G.photo_id=M.id;G.save()
					C+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_F)));return redirect(R)
		else:E=forms.PopupForm(instance=T,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		V=''
		for C in S:
			N=models.photo.objects.get(id=C.photo.id);V=C.judul
			if N.file_path:
				if os.path.isfile(N.file_path.path):
					W=Image.open(N.file_path.path)
					if W:W.close()
			N.delete()
		messages.info(A,mMsgBox.get(_G,V));return redirect(R)
	Q='Popup';c=models.menu.objects.filter(nama=Q,is_admin_menu=_B);d={_K:O.get_menus(),_Q:O.create_breadCrumb(Q),_P:O.find_activeMenuList(Q),_V:D,_U:E,_r:F,_R:get_namaOPD(B),_S:c};return render(A,'account/popup.html',d)
@login_required(login_url=_O)
def komentar(request,mode='',pk='',photoID=''):
	B=mode;A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);G=_I;H=_I;photoID=[]
	if B==_G:
		if pk=='':return HttpResponse(_Y)
		I=crypt_uuid4.ClsCryptUuid4();F=I.dec_text(pk)
		if F=='':return HttpResponse(_Z)
		J=models.comment.objects.filter(site_id=C,id=F)
	if B==_G:
		for K in J:K.delete()
		return redirect('/dashboard/komentar')
	E='Comment';L=models.menu.objects.filter(nama=E,is_admin_menu=_B);M={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_P:D.find_activeMenuList(E),_V:B,_U:G,_r:H,_R:get_namaOPD(C),_S:L};return render(A,'account/comment.html',M)
@login_required(login_url=_O)
def galery_layanan(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-layanan';J=photoID;D=mode;A=request;cek_user(A);C=get_siteID(A);L=menus.ClsMenus(C,_B);E=_I;F=_I;J=[]
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_layanan.objects.filter(site_id=C,id=M);W=models.galery_layanan.objects.filter(site_id=C,id=M)
		for B in W:
			if B.photo.jenis!=_s:J.append(B.photo.id)
	elif D==_N:I=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			E=forms.GaleryLayananForm(A.POST);F=I(A.POST);B=0
			for X in F:
				G=A.POST.get(_M+str(B)+_b);
				if G:
					if models.galery_layanan.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_x,A.POST.get(_F)));
					else:N=A.POST.get(_M+str(B)+_d);O=save_photo_slideshow(B,C,N,G);H=models.galery_layanan.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,photo_id=O.id);return redirect(Q)
				B+=1
		else:E=forms.GaleryLayananForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		S=get_object_or_404(R);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.GaleryLayananForm(A.POST,instance=S);F=I(A.POST)
			if E.is_valid():
				H=E.save(commit=_C);H.site_id=C;H.admin_id=A.user.id;H.save();B=0
				for X in F:
					G=A.POST.get(_M+str(B)+_b)
					if G:N=A.POST.get(_M+str(B)+_d);O=save_photo_slideshow(B,C,N,G);H.photo_id=O.id;H.save()
					B+=1
				messages.info(A,mMsgBox.get(_T,A.POST.get(_F)));return redirect(Q)
		else:E=forms.GaleryLayananForm(instance=S,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=J));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		T=''
		for B in R:
			K=models.photo.objects.get(id=B.photo.id);T=B.judul
			if K.file_path:
				if os.path.isfile(K.file_path.path):
					U=Image.open(K.file_path.path)
					if U:U.close()
			K.delete()
		messages.info(A,mMsgBox.get(_G,T));return redirect(Q)
	P='galeri layanan';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_K:L.get_menus(),_Q:L.create_breadCrumb(P),_P:L.find_activeMenuList(P),_V:D,_U:E,_r:F,_R:get_namaOPD(C),_S:Y};return render(A,'account/galery-layanan.html',Z)
@login_required(login_url=_O)
def galery_video(request,mode='',pk='',photoID=''):
	I='/dashboard/galery-video';C=mode;A=request;cek_user(A);D=get_siteID(A);G=menus.ClsMenus(D,_B);B=_I;photoID=[]
	if C==_L or C==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		K=models.galery_video.objects.filter(site_id=D,id=J)
	if C==_N:
		if A.method==_J:
			B=forms.GaleryVideoForm(A.POST)
			if models.galery_video.objects.filter(site_id=D,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
			else:F=models.galery_video.objects.create(site_id=D,judul=A.POST.get(_F),admin_id=A.user.id,embed=A.POST.get('embed'));return redirect(I)
		else:B=forms.GaleryVideoForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_L:
		E=get_object_or_404(K)
		if A.method==_J:
			B=forms.GaleryVideoForm(A.POST,instance=E)
			if B.is_valid():F=B.save(commit=_C);F.site_id=D;F.admin_id=A.user.id;F.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_F)));return redirect(I)
		else:B=forms.GaleryVideoForm(instance=E,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:E=get_object_or_404(K);M=E.judul;E.delete();messages.info(A,mMsgBox.get(_G,M));return redirect(I)
	H='galeri video';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_K:G.get_menus(),_Q:G.create_breadCrumb(H),_P:G.find_activeMenuList(H),_V:C,_U:B,_R:get_namaOPD(D),_S:N};return render(A,'account/galery-video.html',O)
@login_required(login_url=_O)
def agenda(request,mode='',pk=''):
	H='/dashboard/agenda';D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);C=_I
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.agenda.objects.filter(site_id=E,id=I)
	if D==_N:
		if A.method==_J:
			C=forms.AgendaForm(A.POST,label_suffix='')
			if C.is_valid():
				B=C.save(commit=_C);B.site_id=E;B.admin_id=A.user.id
				if A.POST.get(_AO)!=''and A.POST.get('jam')!='':L=A.POST.get(_AO)+' '+A.POST.get('jam');B.waktu=datetime.strptime(L,'%d/%m/%Y %H:%M')
				B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		B=get_object_or_404(J)
		if A.method==_J:
			C=forms.AgendaForm(A.POST,A.FILES,instance=B,label_suffix='')
			if C.is_valid():O=C.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(instance=B,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:B=get_object_or_404(J);B.delete();messages.info(A,mMsgBox.get(_G,B.nama));return redirect(H)
	G='agenda';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_P:F.find_activeMenuList(G),_V:D,_U:C,_R:get_namaOPD(E),_S:M};return render(A,'account/agenda.html',N)
@login_required(login_url=_O)
def info_hoax(request,mode='',pk=''):
	H='/dashboard/info-hoax';C=mode;A=request;cek_user(A);E=get_siteID(A);
	if not(E==1 or E==68):messages.info(A,_Ab);return redirect(_AC)
	F=menus.ClsMenus(E,_B);B=_I
	if C==_L or C==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.info_hoax.objects.filter(id=I)
	if C==_N:
		if A.method==_J:
			B=forms.InfoHoaxForm(A.POST,label_suffix='')
			if B.is_valid():
				O,L=models.info_hoax.objects.update_or_create(name=A.POST.get(_m),defaults={_j:A.POST.get(_j)})
				if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_m)))
				else:messages.info(A,mMsgBox.get(_T,A.POST.get(_m)))
				return redirect(H)
		else:B=forms.InfoHoaxForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_L:
		D=get_object_or_404(J)
		if A.method==_J:
			B=forms.InfoHoaxForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_T,A.POST.get(_m)));return redirect(H)
		else:B=forms.InfoHoaxForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.name));return redirect(H)
	G='info hoaks';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_P:F.find_activeMenuList(G),_V:C,_U:B,_R:get_namaOPD(E),_S:M};return render(A,'account/info-hoax.html',N)
@login_required(login_url=_O)
def banner_all(request,mode='',pk='',photoID=''):
	T='/dashboard/banner-all';K=photoID;D=mode;A=request;cek_user(A);E=get_siteID(A)
	if not(E==1 or E==68):messages.info(A,_Ab);return redirect(_AC)
	P=menus.ClsMenus(E,_B);C=_I;F=_I;K=[];H=''
	if D==_L or D==_G:
		if pk=='':return HttpResponse(_Y)
		Z=crypt_uuid4.ClsCryptUuid4();H=Z.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		U=models.banner_all.objects.filter(id=H);a=models.banner_all.objects.filter(id=H)
		for B in a:
			if B.photo.jenis!=_s:K.append(B.photo.id)
	elif D==_N:I=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			C=forms.BannerAllForm(A.POST);F=I(A.POST)
			if C.is_valid():
				B=0
				for b in F:
					J=A.POST.get(_M+str(B)+_b)
					if J:
						L=J.replace(_u,'');M=models.photo.Jenis.BANNER_ALL;N=models.photo.objects.create(site_id=E,jenis=M,file_path=L);Q=C.cleaned_data.get('site');G=C.save(commit=_C);G.photo_id=N.id;G.save()
						for R in Q:G.site.add(R)
					B+=1
			return redirect(T)
		else:C=forms.BannerAllForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif D==_L:
		V=get_object_or_404(U);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(K))
		if A.method==_J:
			C=forms.BannerAllForm(A.POST,instance=V);F=I(A.POST)
			if C.is_valid():
				Q=C.cleaned_data.get('site');models.banner_all.site.through.objects.filter(banner_all_id=H).delete();G=C.save();B=0
				for b in F:
					J=A.POST.get(_M+str(B)+_b)
					if J:
						L=J.replace(_u,'');M=models.photo.Jenis.BANNER_ALL;W=A.POST.get(_M+str(B)+_d)
						if W:N,c=models.photo.objects.update_or_create(id=W,defaults={_k:E,_t:M,_q:L})
						else:N,c=models.photo.objects.update_or_create(site_id=E,jenis=M,file_path=L)
						G.photo_id=N.id;G.save()
					B+=1
				for R in Q:G.site.add(R)
				messages.info(A,mMsgBox.get(_T,A.POST.get(_F)));return redirect(T)
		else:C=forms.BannerAllForm(instance=V,label_suffix='');F=I(queryset=models.photo.objects.filter(id__in=K));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		X=''
		for B in U:
			O=models.photo.objects.get(id=B.photo.id);X=B.name
			if O.file_path:
				if os.path.isfile(O.file_path.path):
					Y=Image.open(O.file_path.path)
					if Y:Y.close()
			O.delete()
		messages.info(A,mMsgBox.get(_G,X));return redirect(T)
	S='Banner All';d=models.menu.objects.filter(nama=S,is_admin_menu=_B);e={_K:P.get_menus(),_Q:P.create_breadCrumb(S),_P:P.find_activeMenuList(S),_V:D,_U:C,_r:F,_R:get_namaOPD(E),_S:d};return render(A,'account/banner-all.html',e)
def social_media_ajax(request):
	C=get_siteID(request);A=models.social_media.objects.filter(site_id=C).values(_A,_t,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def instansi_ajax(request):
	C=get_siteID(request);A=models.instansi.objects.filter(site_id=C).values(_A,_E,_AG,'telp',_A5,_AH,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def logo_ajax(request):
	C=get_siteID(request);A=models.logo.objects.filter(site_id=C).values(_A,'position',_v,_D).order_by('-updated_at')
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def banner_ajax(request):
	C=get_siteID(request);A=models.banner.objects.filter(site_id=C).values(_A,'position',_v,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_ajax(request):
	C=get_siteID(request);A=models.menu.objects.filter(site__id=C,is_admin_menu=_C,is_master_menu=_C).values(_A,_E,'href','icon',_w,_D).order_by(_n,_y)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_statis_ajax(request):A=get_siteID(request);B=models.menu.objects.filter(site__id=A,is_statis_menu=_B,is_admin_menu=_C).exclude(href='#').order_by(_n,_y);C=serializers.serialize('json',B,fields=(_A,_E));return HttpResponse(C,content_type='application/json')
def berita_ajax(request):
	C='photo__berita__id';D=get_siteID(request);E={'berita__id':OuterRef(C)};B=models.berita.objects.filter(site_id=D).values(_A,_F,_z,'kategori__nama',_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_z]=Truncator(A[_z]).chars(50)
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
	C='photo__pengumuman__id';D=get_siteID(request);E={'pengumuman__id':OuterRef(C)};B=models.pengumuman.objects.filter(site_id=D).values(_A,_F,_A8,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A8]=Truncator(A[_A8]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def artikel_ajax(request):
	C='photo__artikel__id';D=get_siteID(request);E={'artikel__id':OuterRef(C)};B=models.artikel.objects.filter(site_id=D).values(_A,_F,_A9,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A9]=Truncator(A[_A9]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def dokumen_ajax(request):
	F='extra_field';D='size';B=request;G=get_siteID(B);E=models.dokumen.objects.filter(site_id=G).values(_A,_E,_A0,D,_q,_D)
	for A in E:
		A[_D]=get_natural_datetime(A[_D]);A[D]=naturalsize(A[D]);C=A[_q]
		if'https://'in settings.MEDIA_URL:A[F]='%s%s'%(settings.MEDIA_URL,C)
		else:A[F]='%s://%s%s%s'%(B.scheme,B.get_host(),settings.MEDIA_URL,C)
		A[_q]=Truncator(C).chars(30)
	H=list(E);return JsonResponse(H,safe=_C)
def agenda_ajax(request):
	C=get_siteID(request);B=models.agenda.objects.filter(site_id=C).values(_A,_E,_A0,'lokasi',_AO,'jam','penyelenggara','dihadiri_oleh',_e,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_A0]=Truncator(A[_A0]).words(30)
	D=list(B);return JsonResponse(D,safe=_C)
def pejabat_ajax(request,pIsDefault):
	C=get_siteID(request);A=models.pejabat.objects.filter(site__id=C,is_default=pIsDefault).values(_A,_E,_AN,_v,_D).order_by(_d)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def link_terkait_ajax(request):
	C=get_siteID(request);A=models.link_terkait.objects.filter(site__id=C).values(_A,_E,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def halaman_statis_ajax(request):
	C='photo__halaman_statis__id';D=get_siteID(request);E={'halaman_statis__id':OuterRef(C)};B=models.halaman_statis.objects.filter(site_id=D).values(_A,_F,_A1,'menu__nama',_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A1]=Truncator(A[_A1]).chars(50)
	F=list(B);return JsonResponse(F,safe=_C)
def galery_foto_ajax(request):
	C=get_siteID(request);B=models.galery_foto.objects.filter(site_id=C).values(_A,_F,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def popup_ajax(request):
	C=get_siteID(request);A=models.popup.objects.filter(site_id=C).values(_A,_F,_v,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def komentar_ajax(request):
	C=get_siteID(request);A=models.comment.objects.filter(site_id=C).values(_A,_m,_A5,'body','post__judul',_A2,'active')
	for B in A:B[_A2]=get_natural_datetime(B[_A2])
	D=list(A);return JsonResponse(D,safe=_C)
def galery_layanan_ajax(request):
	C=get_siteID(request);B=models.galery_layanan.objects.filter(site_id=C).values(_A,_F,_e,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def galery_video_ajax(request):
	C=get_siteID(request);B=models.galery_video.objects.filter(site_id=C).values(_A,_F,'embed','embed_video',_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def info_hoax_ajax(request):
	D=get_siteID(request);A=models.info_hoax.objects.all().values(_A,_m,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def banner_all_ajax(request):
	D=get_siteID(request);A=models.banner_all.objects.all().values(_A,_m,_j,_v,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def enc_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.enc_text(data))
def dec_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.dec_text(data))
def toggle_comment_activate(request,pID):A=models.comment.objects.get(id=pID);A.active^=_B;A.save();return HttpResponse('True')
def toggle_comment_activate_all(request):A=models.comment.objects.filter(site_id=get_siteID(request),active=_C).update(active=_B);return HttpResponse('True')
def top_kontributor_berita(request):
	F=models.berita.objects.exclude(admin_id=1).values_list(_AP).annotate(jumlah=Count(_A)).order_by(_AQ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_pengumuman(request):
	F=models.pengumuman.objects.exclude(admin_id=1).values_list(_AP).annotate(jumlah=Count(_A)).order_by(_AQ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_artikel(request):
	F=models.artikel.objects.exclude(admin_id=1).values_list(_AP).annotate(jumlah=Count(_A)).order_by(_AQ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0]);
	return JsonResponse(A,safe=_C)
def site_activity(request):
	D=[];G=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	for A in G:
		B=[];H=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for I in H:B.append(I[_A])
		J=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=B);C=len(B);E=J.filter(is_edited=_B).count()
		if C==0:F=0
		else:F=E/C*100
		K={_A:A[_A],_H:A[_H],_AB:C,_o:E,_A3:F};D.append(K)
	return JsonResponse(D,safe=_C)
def site_activity_pie_chart(request):
	C=[];P=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H));Q=0
	for A in P:
		D=[];R=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for S in R:D.append(S[_A])
		T=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=D);E=len(D);H=T.filter(is_edited=_B).count()
		if E==0:F=0
		else:F=H/E*100
		Q+=F;U={_A:A[_A],_H:A[_H],_AB:E,_o:H,_A3:F};C.append(U)
	C=sorted(C,key=lambda x:x[_A3],reverse=_B);B=[];I=10;J=0;K=0;L=0;M=0;G=_C;N=get_siteID(request);O=0
	for A in C:
		J+=1
		if J<I:
			B.append(A)
			if A[_A]==N:G=_B;
		elif len(B)<=I:
			if G:B.append(A);G=_C;
			elif A[_A]==N:B.append(A)
			else:K+=A[_o];L+=A[_AB];M+=A[_A3];O+=1
		else:K+=A[_o];L+=A[_AB];M+=A[_A3];O+=1
	return JsonResponse(B,safe=_C)
def site_activity_detail(request,siteID):
	B=siteID;C=[];H=[];F=list(models.menu.objects.filter(site__id=B,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AL,_y).values(_A,_E,_w))
	for A in F:
		D=models.halaman_statis.objects.filter(site__id=B,menu__id=A[_A],is_edited=_B)[:1]
		if D:
			for G in D:E={_A:A[_A],_n:A[_w],_K:A[_E],_F:G.judul,_o:1}
		else:E={_A:A[_A],_n:A[_w],_K:A[_E],_F:'',_o:0}
		C.append(E)
	return JsonResponse(C,safe=_C)
def site_activity_detail_pie_chart(request,siteID):
	F=siteID;B=[];L=[];I=list(models.menu.objects.filter(site__id=F,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AL,_y).values(_A,_E,_w))
	for A in I:
		G=models.halaman_statis.objects.filter(site__id=F,menu__id=A[_A],is_edited=_B)[:1]
		if G:
			for J in G:H={_A:A[_A],_n:A[_w],_K:A[_E],_F:J.judul,_o:1}
		else:H={_A:A[_A],_n:A[_w],_K:A[_E],_F:'',_o:0}
		B.append(H)
	E=len(B);C=len(list(filter(lambda x:x[_o]==0,B)));D=len(list(filter(lambda x:x[_o]==1,B)));C=C/E*100;D=D/E*100;K=[{_m:'Menu Terisi','y':D,'sliced':_B,'selected':_B},{_m:'Menu Kosong','y':C}];return JsonResponse(K,safe=_C)
def site_productivity(request):
	B=[];F=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	for A in F:I=[];C=models.berita.objects.filter(site_id=A[_A]).count();D=models.artikel.objects.filter(site_id=A[_A]).count();E=models.pengumuman.objects.filter(site_id=A[_A]).count();G=C+D+E;H={_A:A[_A],_H:A[_H],_f:C,_g:E,_h:D,_c:G};B.append(H)
	B=sorted(B,key=lambda x:x[_c],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[]
	if J==1:L=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		S=list(models.instansi.objects.filter(kategori_id=J).values(_k))
		for A in S:K.append(A[_k])
		L=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_H).values(_A,_H))
	for A in L:W=[];M=models.berita.objects.filter(site_id=A[_A]).count();N=models.artikel.objects.filter(site_id=A[_A]).count();O=models.pengumuman.objects.filter(site_id=A[_A]).count();T=M+N+O;U={_A:A[_A],_H:A[_H],_f:M,_g:O,_h:N,_c:T};C.append(U)
	C=sorted(C,key=lambda x:x[_c],reverse=_B);B=[];P=10;Q=0;D=0;E=0;F=0;G=0;H=_C;R=get_siteID(request);I=0
	for A in C:
		Q+=1
		if Q<P:
			B.append(A)
			if A[_A]==R:H=_B;
		elif len(B)<=P:
			if H:B.append(A);H=_C;
			elif A[_A]==R:B.append(A)
			else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_c];I+=1
		else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_c];I+=1
	V={_A:0,_H:_Ad+str(I)+_Ae,_f:D,_g:E,_h:F,_c:G};B.append(V);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_table(request,kategori_id):
	C=kategori_id;B=[];D=[]
	if C==1:E=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		I=list(models.instansi.objects.filter(kategori_id=C).values(_k))
		for A in I:D.append(A[_k])
		E=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_H).values(_A,_H))
	for A in E:L=[];F=models.berita.objects.filter(site_id=A[_A]).count();G=models.artikel.objects.filter(site_id=A[_A]).count();H=models.pengumuman.objects.filter(site_id=A[_A]).count();J=F+G+H;K={_A:A[_A],_H:A[_H],_f:F,_g:H,_h:G,_c:J};B.append(K)
	B=sorted(B,key=lambda x:x[_c],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kualitas_table(request,kategori_id):
	B=kategori_id;C=[];D=[];E=100;J=50
	if B==1:F=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		K=list(models.instansi.objects.filter(kategori_id=B).values(_k))
		for A in K:D.append(A[_k])
		F=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_H).values(_A,_H))
	for A in F:N=[];G=models.berita.objects.filter(site_id=A[_A],word_count__gte=E).count();H=models.artikel.objects.filter(site_id=A[_A],word_count__gte=E).count();I=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=J).count();L=G+H+I;M={_A:A[_A],_H:A[_H],_f:G,_g:I,_h:H,_c:L};C.append(M)
	return JsonResponse(C,safe=_C)
def kontribusi_kualitas_periode(request,kategori_id,periode_id):
	E=kategori_id;F=[];G=[];H=100;L=50
	if E==1:I=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		B=list(models.instansi.objects.filter(kategori_id=E).values(_k))
		for A in B:G.append(A[_k])
		I=list(models.Site.objects.filter(id__in=G).exclude(id=1).order_by(_H).values(_A,_H))
	C=0;D=0;B=periode_id.split('.')
	if len(B)>=2:C=int(B[0]);D=int(B[1])
	if C and D:
		for A in I:Q=[];J=models.berita.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=H).count();M=models.artikel.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=H).count();N=models.pengumuman.objects.filter(site_id=A[_A],created_at__month=C,created_at__year=D,word_count__gte=L).count();K=J+M+N;O=K/4*100;P={_A:A[_A],_H:A[_H],_c:K,'persentase':O,'ket':''};F.append(P)
	return JsonResponse(F,safe=_C)
def site_kontribusi_kualitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[];L=100;T=50
	if J==1:M=list(models.Site.objects.exclude(id=1).order_by(_H).values(_A,_H))
	else:
		U=list(models.instansi.objects.filter(kategori_id=J).values(_k))
		for A in U:K.append(A[_k])
		M=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_H).values(_A,_H))
	for A in M:Y=[];N=models.berita.objects.filter(site_id=A[_A],word_count__gte=L).count();O=models.artikel.objects.filter(site_id=A[_A],word_count__gte=L).count();P=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=T).count();V=N+O+P;W={_A:A[_A],_H:A[_H],_f:N,_g:P,_h:O,_c:V};C.append(W)
	C=sorted(C,key=lambda x:x[_c],reverse=_B);B=[];Q=10;R=0;D=0;E=0;F=0;G=0;H=_C;S=get_siteID(request);I=0
	for A in C:
		R+=1
		if R<Q:
			B.append(A)
			if A[_A]==S:H=_B;
		elif len(B)<=Q:
			if H:B.append(A);H=_C;
			elif A[_A]==S:B.append(A)
			else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_c];I+=1
		else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_c];I+=1
	X={_A:0,_H:_Ad+str(I)+_Ae,_f:D,_g:E,_h:F,_c:G};B.append(X);return JsonResponse(B,safe=_C)
def site_ajax(request):
	A=request.GET.get(_AT)
	if A:B=models.Site.objects.filter(domain__icontains=A).exclude(id=1).values(_A,text=F(_H))
	else:B=models.Site.objects.exclude(id=1).values(_A,text=F(_H))
	return JsonResponse({_AU:list(B),_AV:{'more':_B}},safe=_C)
def instansi_kategori_ajax(request):
	A=request.GET.get(_AT)
	if A:B=models.instansi_kategori.objects.filter(nama__icontains=A).values(_A,text=F(_E))
	else:B=models.instansi_kategori.objects.values(_A,text=F(_E))
	return JsonResponse({_AU:list(B),_AV:{'more':_B}},safe=_C)
def post_range(request):
	G='month';E=request.GET.get(_AT);B=[]
	if E:
		C=models.berita.objects.datetimes(_A2,G,tzinfo=timezone.utc)
		for A in C:
			F=A.strftime(_A4)
			if E in F:D={_A:str(A.month)+'.'+str(A.year),_p:F};B.append(D)
	else:
		C=models.berita.objects.datetimes(_A2,G,tzinfo=timezone.utc)
		for A in reversed(C):D={_A:str(A.month)+'.'+str(A.year),_p:A.strftime(_A4)};B.append(D)
	return JsonResponse({_AU:B,_AV:{'more':_B}},safe=_C)