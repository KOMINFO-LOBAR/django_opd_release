_AT='pagination'
_AS=' Instansi)'
_AR='Lainnya ('
_AQ='not found'
_AP='Menu tidak dapat diakses dari user Anda!'
_AO='str_foto_path = '
_AN='mChartNews'
_AM='mChartHit'
_AL='mFound = False '
_AK='mFound = True '
_AJ='-jumlah'
_AI='admin'
_AH='tanggal'
_AG='jabatan'
_AF='/dashboard/pejabat'
_AE='parent_id'
_AD='form_img'
_AC='photo_id'
_AB='photo-str_file_path'
_AA='kode_post'
_A9='alamat'
_A8='/dashboard/dashboard'
_A7='total_menu'
_A6='/dashboard/link-terkait'
_A5='isi_artikel'
_A4='isi_pengumuman'
_A3='/dashboard/menu'
_A2='photo'
_A1='email'
_A0='persen'
_z='isi_halaman'
_y='deskripsi'
_x='isi_berita'
_w='order_menu'
_v='potential_duplicate_add'
_u='parent__nama'
_t='photo__file_path'
_s='media/'
_r='jenis'
_q='formset_img'
_p='terisi'
_o='parent'
_n='file_path'
_m='name'
_l='site_id'
_k='save foto complete '
_j='link'
_i='username'
_h='artikel'
_g='pengumuman'
_f='berita'
_e='status'
_d='total'
_c='-id'
_b='-str_file_path'
_a='form_edit'
_Z='Parameter Primary Key tidak ditemukan!'
_Y='Parameter Primary Key tidak tersedia'
_X='save_add'
_W='form_add'
_V='mode'
_U='form'
_T='menu_aktif'
_S='namaOPD'
_R='activeMenuList'
_Q='breadCrumb'
_P='save_edit'
_O='/account/login'
_N='add'
_M='form-'
_L='menu'
_K='edit'
_J='POST'
_I='domain'
_H=None
_G='delete'
_F='judul'
_E='nama'
_D='updated_at'
_C=False
_B=True
_A='id'
import calendar,io,os,re,unicodedata
from datetime import datetime
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
mMsgBox=msgbox.ClsMsgBox()
def unicode_to_string(value):B='ascii';A=value;A=str(A);A=unicodedata.normalize('NFKD',A).encode(B,'ignore').decode(B);return A
def redirect_to_login(request):
	if request.user.is_authenticated:return redirect(_A8)
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
	G=request;H=get_siteID(G);L=G.get_host();J=datetime.now();B=ContentType.objects.get(app_label='sites',model='site');B=B.id if B else _H;C=HitCount.objects.filter(content_type_id=B,object_pk=H).first();C=C.id if C else _H;I=[];E={};D='';F=0
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
def dashboard(request):A=request;cek_user(A);D=get_siteID(A);B=menus.ClsMenus(D,_B);E=get_hit_count(A);F=get_news_count(A);C='analytics';G=models.menu.objects.filter(nama=C,is_admin_menu=_B);H={_L:B.get_menus(),_Q:B.create_breadCrumb(C),_R:B.find_activeMenuList(C),_S:get_namaOPD(D),_T:G,_AM:E,_AN:F};return render(A,'account/dashboard.html',H)
@login_required(login_url=_O)
def dashboard_detail(request):
	G='text';B=request;cek_user(B);C=get_siteID(B);E=menus.ClsMenus(C,_B);I=models.berita.objects.exclude(site_id=1).count();J=models.artikel.objects.exclude(site_id=1).count();K=models.pengumuman.objects.exclude(site_id=1).count();H=models.Site.objects.get(id=C);L={_A:H.id,G:H.domain};D={};A=models.instansi.objects.filter(site_id=C)
	if A:
		A=A.get()
		if A.kategori:D={_A:A.kategori.id,G:A.kategori.nama}
	if not D:A=models.instansi_kategori.objects.get(id=1);D={_A:A.id,G:A.nama}
	print('form_data_kategori = ');print(D);M=get_hit_count(B);N=get_news_count(B);F='monitoring';O=models.menu.objects.filter(nama=F,is_admin_menu=_B);P={_L:E.get_menus(),_Q:E.create_breadCrumb(F),_R:E.find_activeMenuList(F),_S:get_namaOPD(C),_T:O,_AM:M,_AN:N,'mGrandTotal':I+K+J,'siteid':C,'form_data':L,'form_data_kategori':D};return render(B,'account/dashboard-detail.html',P)
def register(request):
	A=request
	if A.method==_J:
		B=CustomUserCreationForm(A.POST)
		if B.is_valid():C=B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_i)));return redirect(_O)
	else:B=forms.CustomUserCreationForm(label_suffix='')
	return render(A,'account/register.html',{_U:B})
@login_required(login_url=_O)
def social_media(request,mode='',pk=''):
	H='/dashboard/social-media';C=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_H
	if C==_K or C==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.social_media.objects.filter(site_id=E,id=I)
	if C==_N:
		if A.method==_J:
			B=forms.SocialMediaForm(A.POST,label_suffix='')
			if B.is_valid():
				if models.social_media.objects.filter(site_id=E,link=A.POST.get(_j)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_j)))
				else:
					L=models.social_media.objects.create(site_id=E,jenis=A.POST.get(_r),link=A.POST.get(_j))
					if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_r)))
					return redirect(H)
		else:B=forms.SocialMediaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_K:
		D=get_object_or_404(J)
		if A.method==_J:
			B=forms.SocialMediaForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_r)));return redirect(H)
		else:B=forms.SocialMediaForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.jenis));return redirect(H)
	G='social media';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(E),_T:M};return render(A,'account/social-media.html',N)
@login_required(login_url=_O)
def instansi(request,mode='',pk=''):
	I='/dashboard/instansi';C=mode;A=request;cek_user(A);D=get_siteID(A);E=menus.ClsMenus(D,_B);B=_H
	if C==_K:
		if pk=='':return HttpResponse(_Y)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		K=models.instansi.objects.filter(site_id=D,id=H)
	if C==_N:
		if A.method==_J:
			B=forms.InstansiForm(A.POST,label_suffix='')
			if B.is_valid():
				L=models.User.objects.get(id=A.user.id);M,N=models.instansi.objects.update_or_create(site_id=D,defaults={_E:A.POST.get(_E),_A9:A.POST.get(_A9),'telp':A.POST.get('telp'),_A1:A.POST.get(_A1),_AA:A.POST.get(_AA)});M.admin.add(L)
				if N:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect(I)
		else:B=forms.InstansiForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_K:
		F=get_object_or_404(K)
		if A.method==_J:
			B=forms.InstansiForm(A.POST,instance=F,label_suffix='')
			if B.is_valid():F.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(I)
		else:B=forms.InstansiForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	G='instansi';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:E.get_menus(),_Q:E.create_breadCrumb(G),_R:E.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(D),_T:O};return render(A,'account/instansi.html',P)
@login_required(login_url=_O)
def logo(request,mode='',pk=''):
	K='logo';J='Logo ';C='logo-position';A=request;cek_user(A);B=get_siteID(A);D=menus.ClsMenus(B,_B);E=_H;F=_H
	if mode==_N:
		if A.method==_J:
			E=forms.LogoForm(A.POST);F=forms.PhotoForm(A.POST)
			if A.POST.get(C).upper()=='TOP':H=models.photo.Jenis.LOGO_TOP
			else:H=models.photo.Jenis.LOGO_BOTTOM
			I=A.POST.get(_AB)
			if I:
				L=I.replace(_s,'');M,N=models.photo.objects.update_or_create(site_id=B,jenis=H,defaults={_n:L});Q,R=models.logo.objects.update_or_create(site_id=B,position=A.POST.get(C),defaults={_AC:M.id})
				if N:messages.info(A,mMsgBox.get(_X,J+A.POST.get(C)))
				else:messages.info(A,mMsgBox.get(_P,J+A.POST.get(C)))
			return redirect('/dashboard/logo')
		else:E=forms.LogoForm(label_suffix='',prefix=K);F=forms.PhotoForm(label_suffix='',prefix=_A2);messages.info(A,mMsgBox.get(_W))
	G=K;O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:D.get_menus(),_Q:D.create_breadCrumb(G),_R:D.find_activeMenuList(G),_V:mode,_U:E,_AD:F,_S:get_namaOPD(B),_T:O};return render(A,'account/logo.html',P)
@login_required(login_url=_O)
def banner(request,mode='',pk=''):
	J='banner';A=request;cek_user(A);C=get_siteID(A);E=menus.ClsMenus(C,_B);F=_H;G=_H
	if mode==_N:
		if A.method==_J:
			F=forms.BannerForm(A.POST);G=forms.PhotoForm(A.POST);B=A.POST.get('banner-str_banner_position')
			if B=='bottom':D=models.photo.Jenis.BANNER_BOTTOM
			elif B=='middle1':D=models.photo.Jenis.BANNER_MIDDLE1
			elif B=='middle2':D=models.photo.Jenis.BANNER_MIDDLE2
			else:D=models.photo.Jenis.BANNER_TOP
			H=A.POST.get(_AB);print(_AO);print(H)
			if H:
				K=H.replace(_s,'');L,M=models.photo.objects.update_or_create(site_id=C,jenis=D,defaults={_n:K});P,Q=models.banner.objects.update_or_create(site_id=C,position=B,defaults={_AC:L.id,_j:A.POST.get('banner-link')})
				if M:messages.info(A,mMsgBox.get(_X,B))
				else:messages.info(A,mMsgBox.get(_P,B))
			return redirect('/dashboard/banner')
		else:F=forms.BannerForm(label_suffix='',prefix=J);G=forms.PhotoForm(label_suffix='',prefix=_A2);messages.info(A,mMsgBox.get(_W))
	I=J;N=models.menu.objects.filter(nama=I,is_admin_menu=_B);O={_L:E.get_menus(),_Q:E.create_breadCrumb(I),_R:E.find_activeMenuList(I),_V:mode,_U:F,_AD:G,_S:get_namaOPD(C),_T:N};return render(A,'account/banner.html',O)
def menu_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.menu.objects.filter(is_master_menu=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('menu_refresh'));return redirect(_A3)
def menu_update_visibled(request,pk,is_visible):
	A=models.Site.objects.get(id=get_siteID(request));B=models.menu.objects.get(id=pk)
	if is_visible:B.site.add(A)
	else:B.site.remove(A)
	return HttpResponse('True')
def menu_is_have_child(menu_id):return models.menu.objects.filter(parent__id=menu_id).exists()
@login_required(login_url=_O)
def menu(request,mode='',pk=''):
	U='delete_fail';T='master_menu';S='is_master_menu';D=mode;A=request;cek_user(A);E=get_siteID(A);J=menus.ClsMenus(E,_B);C=_H;L=_H;F=_H
	if D=='':V=menus.ClsMenus(E,_C,_B);L=V.get_menus()
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();M=W.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		N=models.menu.objects.filter(site__id=E,id=M)
	if D==_N or D==_o:
		if D==_o:F=pk
		if A.method==_J:
			C=forms.MenuForm(A.POST,label_suffix='')
			if C.is_valid():
				G=models.Site.objects.get(id=E);F=A.POST.get(_o)
				if not F:F=_H
				O=_B;P=models.menu.objects.filter(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F).values_list(S,flat=_B)
				if P.count()>0:
					if P[0]==_B:messages.info(A,mMsgBox.get(T));C=forms.MenuForm(label_suffix='');O=_C
				if O:
					X,Y=models.menu.objects.update_or_create(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F,defaults={_E:A.POST.get(_E),'href':'menu/'+slugify(A.POST.get(_E)),'icon':A.POST.get('icon'),_w:A.POST.get(_w),'is_visibled':_B,'is_statis_menu':_B});X.site.add(G)
					if Y:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
					return redirect(_A3)
		else:C=forms.MenuForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		B=get_object_or_404(N)
		if A.method==_J:
			C=forms.MenuForm(A.POST,instance=B,label_suffix='')
			if A.POST.get(_o)==str(B.id):messages.info(A,mMsgBox.get('circular_menu'));C=forms.MenuForm(instance=B,label_suffix='')
			elif A.POST.get(S):messages.info(A,mMsgBox.get(T));C=forms.MenuForm(instance=B,label_suffix='')
			elif C.is_valid():B=C.save(commit=_C);B.is_statis_menu=1;B.is_visibled=1;B.save();G=models.Site.objects.get(id=E);B.site.add(G);messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(_A3)
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
		return redirect(_A3)
	K=_L;b=models.menu.objects.filter(nama=K,is_admin_menu=_B);c={_L:J.get_menus(),_Q:J.create_breadCrumb(K),_R:J.find_activeMenuList(K),_V:D,_U:C,'menu_master':L,_AE:F,_S:get_namaOPD(E),_T:b};return render(A,'account/menu.html',c)
def delete_photo(request):
	print('inside delete photo');C=range(3)
	for B in C:
		A=request.POST.get('file_path_'+str(B));print(A)
		if A!='':
			if os.path.isfile(A):os.remove(A);print('remove photo success '+str(B))
	return HttpResponse('OKE')
def upload_photo(request,width,height):
	O='JPEG';N='RGBA';M='image/png';J='/';I='.jpg';G=request;A=G.FILES.get(_A2);H=G.POST.get('old_photo')
	if H:
		if os.path.isfile(H):os.remove(H);print('remove photo success')
	P=get_siteID(G);Q=Image.open(io.BytesIO(A.read()));B=Q.resize((width,height),Image.ANTIALIAS);F=datetime.now();R=str(P)+'-'+F.strftime('%Y%m%d-%H%M%S-%f');S=F.strftime('%Y');T=F.strftime('%m');U=F.strftime('%d')
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
	B=idx;A=_H
	if B==0:A=models.photo.Jenis.HIGHLIGHT1
	elif B==1:A=models.photo.Jenis.HIGHLIGHT2
	elif B==2:A=models.photo.Jenis.HIGHLIGHT3
	return A
def save_photo_slideshow(idx,site_id,photo_id,str_foto_path):
	C=photo_id;B=site_id;print('Begin INSPECT');D=get_photo_kind(idx);print('mode add/edit PHOTO IDs == ');print(C);E=str_foto_path;print('str_foto_path_replace');print(E);print(_r);print(D);print('siteid');print(B)
	if C:A=models.photo.objects.get(id=C);A.site_id=B;A.jenis=D;A.file_path=E;A.save();print('[save_photo_slideshow] - Update foto complete')
	else:A=models.photo.objects.create(site_id=B,jenis=D,file_path=E);print('[save_photo_slideshow] - save foto complete')
	print('END INSPECT');return A
def save_tags(tag_list,obj_master):
	C=obj_master;B=tag_list;models.berita.tags.through.objects.filter(berita_id=C.id).delete();A=0
	while A<len(B):D=models.tags.objects.get(id=B[A]);C.tags.add(D);A+=1
@login_required(login_url=_O)
def berita(request,mode='',pk='',photoID=''):
	W='/dashboard/berita';N=photoID;G=mode;A=request;cek_user(A);F=get_siteID(A);Q=menus.ClsMenus(F,_B);D=_H;H=_H;N=[]
	if G==_K or G==_G:
		if pk=='':return HttpResponse(_Y)
		Z=crypt_uuid4.ClsCryptUuid4();O=Z.dec_text(pk)
		if O=='':return HttpResponse(_Z)
		X=models.berita.objects.filter(site_id=F,id=O);R=models.berita.photo.through.objects.filter(berita__site=F,berita__id=O)
		for B in R:N.append(B.photo.id)
	elif G==_N:J=formset_factory(forms.PhotoForm,extra=3)
	if G==_N:
		if A.method==_J:
			D=forms.BeritaForm(A.POST);H=J(A.POST)
			if D.is_valid():
				C=A.POST.get(_F);E=A.POST.get(_x)
				if not C.isascii():print('is unicode');C=unicode_to_string(C)
				print('judul=',C)
				if not E.isascii():print('isi berita is contain unicode');E=unicode_to_string(E)
				print('isi berita =',E);S=models.berita.objects.create(site_id=F,judul=C,admin_id=A.user.id,kategori_id=A.POST.get('kategori'),isi_berita=E,status=A.POST.get(_e));T=A.POST.getlist('tags');save_tags(T,S);B=0
				for a in H:
					K=A.POST.get(_M+str(B)+_b)
					if K:
						U=A.POST.get(_M+str(B)+_c);P=save_photo_slideshow(B,F,U,K)
						if P:S.photo.add(P);print(_k+str(B))
					B+=1
				if S:messages.info(A,mMsgBox.get(_X,C))
				return redirect(W)
		else:D=forms.BeritaForm(label_suffix='');H=J();messages.info(A,mMsgBox.get(_W))
	elif G==_K:
		L=get_object_or_404(X);J=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_J:
			D=forms.BeritaForm(A.POST,instance=L);H=J(A.POST)
			if D.is_valid():
				E=D.cleaned_data.get(_x)
				if not E.isascii():E=unicode_to_string(E)
				C=D.cleaned_data.get(_F)
				if not C.isascii():C=unicode_to_string(C)
				I=D.save(commit=_C);I.judul=C;I.isi_berita=E;I.site_id=F;I.admin_id=A.user.id;I.save();T=A.POST.getlist('tags');save_tags(T,I);B=0
				for a in H:
					K=A.POST.get(_M+str(B)+_b)
					if K!='':U=A.POST.get(_M+str(B)+_c);P=save_photo_slideshow(B,F,U,K);I.photo.add(P);print(_k+str(B))
					B+=1
				messages.info(A,mMsgBox.get(_P,C));return redirect(W)
		else:D=forms.BeritaForm(instance=L,label_suffix='');H=J(queryset=models.photo.objects.filter(id__in=N));messages.info(A,mMsgBox.get(_a))
	elif G==_G:
		for B in R:
			M=models.photo.objects.get(id=B.photo.id)
			if M.file_path:
				print('obj_img.file_path = ');print(M.file_path)
				if os.path.exists(M.file_path.path):
					Y=Image.open(M.file_path.path)
					if Y:Y.close()
			M.delete()
		R=models.berita.photo.through.objects.filter(berita__site=F,berita__id=O).delete();L=get_object_or_404(X);L.delete();messages.info(A,mMsgBox.get(_G,L.judul));return redirect(W)
	V=_f;b=models.menu.objects.filter(nama=V,is_admin_menu=_B);c={_L:Q.get_menus(),_Q:Q.create_breadCrumb(V),_R:Q.find_activeMenuList(V),_V:G,_U:D,_q:H,_S:get_namaOPD(F),_T:b};return render(A,'account/berita.html',c)
@login_required(login_url=_O)
def kategori(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_H
	if mode==_N:
		if A.method==_J:
			B=forms.KategoriForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.kategori.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect('/dashboard/kategori')
		else:B=forms.KategoriForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='kategori';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:mode,_U:B,_S:get_namaOPD(C),_T:I};return render(A,'account/kategori.html',J)
@login_required(login_url=_O)
def tags(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_H
	if mode==_N:
		if A.method==_J:
			B=forms.TagsForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.tags.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect('/dashboard/tags')
		else:B=forms.TagsForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='tags';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:mode,_U:B,_S:get_namaOPD(C),_T:I};return render(A,'account/tags.html',J)
@login_required(login_url=_O)
def pengumuman(request,mode='',pk=''):
	W='Pengumuman';S='/dashboard/pengumuman';D=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);E=_H;F=_H;N=[]
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		X=crypt_uuid4.ClsCryptUuid4();J=X.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		T=models.pengumuman.objects.filter(site_id=C,id=J);O=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=J)
		for B in O:N.append(B.photo.id)
	elif D==_N:G=formset_factory(forms.PhotoForm,extra=3)
	if D==_N:
		if A.method==_J:
			E=forms.PengumumanForm(A.POST);F=G(A.POST)
			if models.pengumuman.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_F)))
			else:
				U=models.pengumuman.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_pengumuman=A.POST.get(_A4),status=A.POST.get(_e));B=0
				for Y in F:
					H=A.POST.get(_M+str(B)+_b)
					if H:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);U.photo.add(Q);print(_k+str(B))
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,W))
				return redirect(S)
		else:E=forms.PengumumanForm(label_suffix='');F=G();messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		I=get_object_or_404(T);G=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_J:
			E=forms.PengumumanForm(A.POST,instance=I);F=G(A.POST)
			if E.is_valid():
				K=E.save(commit=_C);K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for Y in F:
					H=A.POST.get(_M+str(B)+_b)
					if H:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);K.photo.add(Q);print(_k+str(B))
					B+=1
			messages.info(A,mMsgBox.get(_P,W));return redirect(S)
		else:E=forms.PengumumanForm(instance=I,label_suffix='');F=G(queryset=models.photo.objects.filter(id__in=N));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		for B in O:
			L=models.photo.objects.get(id=B.photo.id)
			if L.file_path:
				if os.path.isfile(L.file_path.path):
					V=Image.open(L.file_path.path)
					if V:V.close()
			L.delete()
		O=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=J).delete();I=get_object_or_404(T);I.delete();messages.info(A,mMsgBox.get(_G,I.judul));return redirect(S)
	R=_g;Z=models.menu.objects.filter(nama=R,is_admin_menu=_B);a={_L:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:D,_U:E,_q:F,_S:get_namaOPD(C),_T:Z};return render(A,'account/pengumuman.html',a)
@login_required(login_url=_O)
def artikel(request,mode='',pk=''):
	S='/dashboard/artikel';D=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);E=_H;F=_H;N=[]
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();J=W.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		T=models.artikel.objects.filter(site_id=C,id=J);O=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=J)
		for B in O:N.append(B.photo.id)
	elif D==_N:G=formset_factory(forms.PhotoForm,extra=3)
	if D==_N:
		if A.method==_J:
			E=forms.ArtikelForm(A.POST);F=G(A.POST)
			if models.artikel.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_F)))
			else:
				U=models.artikel.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_artikel=A.POST.get(_A5),status=A.POST.get(_e));B=0
				for X in F:
					H=A.POST.get(_M+str(B)+_b)
					if H:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);U.photo.add(Q);print(_k+str(B))
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
				return redirect(S)
		else:E=forms.ArtikelForm(label_suffix='');F=G();messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		I=get_object_or_404(T);G=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_J:
			E=forms.ArtikelForm(A.POST,instance=I);F=G(A.POST)
			if E.is_valid():
				K=E.save(commit=_C);K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for X in F:
					H=A.POST.get(_M+str(B)+_b)
					if H:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);K.photo.add(Q);print(_k+str(B))
					B+=1
			messages.info(A,mMsgBox.get(_P,'Artikel'));return redirect(S)
		else:E=forms.ArtikelForm(instance=I,label_suffix='');F=G(queryset=models.photo.objects.filter(id__in=N));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		for B in O:
			L=models.photo.objects.get(id=B.photo.id)
			if L.file_path:
				if os.path.isfile(L.file_path.path):
					V=Image.open(L.file_path.path)
					if V:V.close()
			L.delete()
		O=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=J).delete();I=get_object_or_404(T);I.delete();messages.info(A,mMsgBox.get(_G,I.judul));return redirect(S)
	R=_h;Y=models.menu.objects.filter(nama=R,is_admin_menu=_B);Z={_L:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:D,_U:E,_q:F,_S:get_namaOPD(C),_T:Y};return render(A,'account/artikel.html',Z)
def pejabat_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.pejabat.objects.filter(is_default=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('pejabat_refresh'));return redirect(_AF)
@login_required(login_url=_O)
def pejabat(request,mode='',pk=''):
	C=mode;A=request;cek_user(A);B=get_siteID(A);F=menus.ClsMenus(B,_B);D=_H;G=_H
	if C==_K or C==_G:
		if pk=='':return HttpResponse(_Y)
		M=crypt_uuid4.ClsCryptUuid4();J=M.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		N=models.pejabat.objects.filter(site__id=B,id=J)
	if C==_N:
		if A.method==_J:
			D=forms.PejabatForm(A.POST);G=forms.PhotoForm(A.POST);O=models.photo.Jenis.PEJABAT_OPD
			if D.is_valid():
				K=A.POST.get(_AB)
				if K:
					P=K.replace(_s,'');Q,R=models.photo.objects.update_or_create(site_id=B,jenis=O,defaults={_n:P});print('siteID',B);print('models.pejabat.Position.PEJABAT_OPD',models.pejabat.Position.PEJABAT_OPD);L,S=models.pejabat.objects.update_or_create(site__id=B,jabatan_index=models.pejabat.Position.PEJABAT_OPD,defaults={_AC:Q.id,_E:A.POST.get(_E),_AG:A.POST.get(_AG),'admin_id':A.user.id,'is_default':0});print(L,S);T=models.Site.objects.get(id=B);L.site.add(T)
					if R:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect(_AF)
		else:D=forms.PejabatForm(label_suffix='');G=forms.PhotoForm(label_suffix='',prefix=_A2);messages.info(A,mMsgBox.get(_W))
	elif C==_G:
		E=get_object_or_404(N);print('post = ');print(E.photo.id);H=models.photo.objects.filter(id=E.photo.id);print('foto = ');print(H)
		if H:H.delete()
		E.delete();messages.info(A,mMsgBox.get(_G,E.nama));return redirect(_AF)
	I='pejabat';U=models.menu.objects.filter(nama=I,is_admin_menu=_B);V={_L:F.get_menus(),_Q:F.create_breadCrumb(I),_R:F.find_activeMenuList(I),_V:C,_U:D,_AD:G,_S:get_namaOPD(B),_T:U};return render(A,'account/pejabat.html',V)
def link_terkait_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.link_terkait.objects.all()
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('link_terkait_refresh'));return redirect(_A6)
@login_required(login_url=_O)
def link_terkait(request,mode='',pk=''):
	D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_H
	if D==_K or D==_G:
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
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect(_A6)
		else:B=forms.LinkTerkaitForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		C=get_object_or_404(I)
		if A.method==_J:
			B=forms.LinkTerkaitForm(A.POST,instance=C,label_suffix='')
			if B.is_valid():C.save();N=models.Site.objects.get(id=E);C.site.add(N);messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(_A6)
		else:B=forms.LinkTerkaitForm(instance=C,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:C=get_object_or_404(I);C.delete();messages.info(A,mMsgBox.get(_G,C.nama));return redirect(_A6)
	G='link terkait';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:D,_U:B,_S:get_namaOPD(E),_T:O};return render(A,'account/link-terkait.html',P)
@login_required(login_url=_O)
def dokumen(request,mode='',pk=''):
	I='/dashboard/dokumen';D=mode;A=request;cek_user(A);E=get_siteID(A);G=menus.ClsMenus(E,_B);C=_H
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		K=models.dokumen.objects.filter(site_id=E,id=J)
	if D==_N:
		if A.method==_J:
			C=forms.DokumenForm(A.POST,A.FILES,label_suffix='')
			if C.is_valid():
				M=A.FILES.get(_n)
				if models.dokumen.objects.filter(site_id=E,nama__iexact=A.POST.get(_E)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_E)))
				else:
					B=models.dokumen.objects.create(site_id=E,nama=A.POST.get(_E),admin_id=A.user.id,file_path=M,deskripsi=A.POST.get(_y),status=A.POST.get(_e));B.size=os.stat(B.file_path.path).st_size;B.save()
					if B:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					return redirect(I)
		else:C=forms.DokumenForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		F=get_object_or_404(K)
		if A.method==_J:
			C=forms.DokumenForm(A.POST,A.FILES,instance=F,label_suffix='')
			if C.is_valid():
				B=C.save()
				if os.path.isfile(B.file_path.path):B.size=os.stat(B.file_path.path).st_size;B.save()
				messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(I)
		else:C=forms.DokumenForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:F=get_object_or_404(K);F.delete();messages.info(A,mMsgBox.get(_G,F.nama));return redirect(I)
	H='dokumen';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_L:G.get_menus(),_Q:G.create_breadCrumb(H),_R:G.find_activeMenuList(H),_V:D,_U:C,_S:get_namaOPD(E),_T:N};return render(A,'account/dokumen.html',O)
@login_required(login_url=_O)
def halaman_statis(request,mode='',pk=''):
	S='/dashboard/halaman-statis';E=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);D=_H;F=_H;N=[]
	if E==_K or E==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();K=V.dec_text(pk)
		if K=='':return HttpResponse(_Z)
		T=models.halaman_statis.objects.filter(site_id=C,id=K);O=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=K)
		for B in O:N.append(B.photo.id)
	elif E==_N:H=formset_factory(forms.PhotoForm,extra=3)
	if E==_N:
		if A.method==_J:
			D=forms.HalamanStatisForm(A.POST);F=H(A.POST)
			if D.is_valid():
				if models.halaman_statis.objects.filter(site_id=C,menu_id=A.POST.get(_L)).count()>1:messages.info(A,mMsgBox.get('menu_already_exists'))
				else:
					G,Z=models.halaman_statis.objects.update_or_create(site_id=C,menu_id=A.POST.get(_L),defaults={_l:C,_F:A.POST.get(_F),_z:A.POST.get(_z),'admin_id':A.user.id,'is_edited':_B});B=0
					for W in F:
						I=A.POST.get(_M+str(B)+_b)
						if I:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,I);G.photo.add(Q);print(_k+str(B))
						B+=1
					messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif E==_K:
		J=get_object_or_404(T);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_J:
			D=forms.HalamanStatisForm(A.POST,instance=J);F=H(A.POST)
			if D.is_valid():
				G=D.save(commit=_C);G.site_id=C;G.admin_id=A.user.id;G.is_edited=_B;G.save();B=0
				for W in F:
					I=A.POST.get(_M+str(B)+_b)
					if I:P=A.POST.get(_M+str(B)+_c);Q=save_photo_slideshow(B,C,P,I);G.photo.add(Q);print(_k+str(B))
					B+=1
				messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(instance=J,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=N));messages.info(A,mMsgBox.get(_a))
	elif E==_G:
		for B in O:
			L=models.photo.objects.get(id=B.photo.id)
			if L.file_path:
				if os.path.isfile(L.file_path.path):
					U=Image.open(L.file_path.path)
					if U:U.close()
			L.delete()
		O=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=K).delete();J=get_object_or_404(T);J.delete();messages.info(A,mMsgBox.get(_G,J.judul));return redirect(S)
	R='halaman statis';X=models.menu.objects.filter(nama=R,is_admin_menu=_B);Y={_L:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:E,_U:D,_q:F,_S:get_namaOPD(C),_T:X};return render(A,'account/halaman-statis.html',Y)
@login_required(login_url=_O)
def galery_foto(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-foto';J=photoID;C=mode;A=request;cek_user(A);D=get_siteID(A);L=menus.ClsMenus(D,_B);E=_H;F=_H;J=[];print('mode = ');print(C)
	if C==_K or C==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_foto.objects.filter(site_id=D,id=M);W=models.galery_foto.objects.filter(site_id=D,id=M)
		for B in W:J.append(B.photo.id)
	elif C==_N:H=formset_factory(forms.PhotoForm)
	if C==_N:
		if A.method==_J:
			E=forms.GaleryFotoForm(A.POST);F=H(A.POST);B=0
			for X in F:
				G=A.POST.get(_M+str(B)+_b);print(_AO);print(G)
				if G:N=A.POST.get(_M+str(B)+_c);O=save_photo_slideshow(B,D,N,G);print(_k+str(B));a=models.galery_foto.objects.create(site_id=D,judul=A.POST.get(_F),admin_id=A.user.id,photo_id=O.id)
				B+=1
			return redirect(Q)
		else:E=forms.GaleryFotoForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif C==_K:
		S=get_object_or_404(R);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.GaleryFotoForm(A.POST,instance=S);F=H(A.POST)
			if E.is_valid():
				print('yes form is valid');I=E.save(commit=_C);I.site_id=D;I.admin_id=A.user.id;I.save();B=0
				for X in F:
					G=A.POST.get(_M+str(B)+_b)
					if G:N=A.POST.get(_M+str(B)+_c);O=save_photo_slideshow(B,D,N,G);print(_k+str(B));I.photo_id=O.id;I.save()
					B+=1
				messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(Q)
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
	P='galeri foto';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_L:L.get_menus(),_Q:L.create_breadCrumb(P),_R:L.find_activeMenuList(P),_V:C,_U:E,_q:F,_S:get_namaOPD(D),_T:Y};return render(A,'account/galery-foto.html',Z)
@login_required(login_url=_O)
def popup(request,mode='',pk='',photoID=''):
	X='published';R='/dashboard/popup';J=photoID;D=mode;A=request;cek_user(A);B=get_siteID(A);O=menus.ClsMenus(B,_B);E=_H;F=_H;J=[]
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		Y=crypt_uuid4.ClsCryptUuid4();P=Y.dec_text(pk)
		if P=='':return HttpResponse(_Z)
		S=models.popup.objects.filter(site_id=B,id=P);Z=models.popup.objects.filter(site_id=B,id=P)
		for C in Z:J.append(C.photo.id)
	elif D==_N:H=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			E=forms.PopupForm(A.POST);F=H(A.POST);C=0
			for a in F:
				I=A.POST.get(_M+str(C)+_b)
				if I:
					K=I.replace(_s,'');L=models.photo.Jenis.POPUP
					if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
					if models.popup.objects.filter(site_id=B,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_F)))
					else:M=models.photo.objects.create(site_id=B,jenis=L,file_path=K);G=models.popup.objects.create(site_id=B,judul=A.POST.get(_F),admin_id=A.user.id,status=A.POST.get(_e),photo_id=M.id)
				C+=1
			return redirect(R)
		else:E=forms.PopupForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		T=get_object_or_404(S);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.PopupForm(A.POST,instance=T);F=H(A.POST)
			if E.is_valid():
				if A.POST.get(_e)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
				G=E.save(commit=_C);G.site_id=B;G.admin_id=A.user.id;G.save();C=0
				for a in F:
					I=A.POST.get(_M+str(C)+_b)
					if I:
						K=I.replace(_s,'');L=models.photo.Jenis.POPUP;U=A.POST.get(_M+str(C)+_c)
						if U:M,b=models.photo.objects.update_or_create(id=U,defaults={_l:B,_r:L,_n:K})
						else:M,b=models.photo.objects.update_or_create(site_id=B,jenis=L,file_path=K)
						G.photo_id=M.id;G.save()
					C+=1
				messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(R)
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
	Q='Popup';c=models.menu.objects.filter(nama=Q,is_admin_menu=_B);d={_L:O.get_menus(),_Q:O.create_breadCrumb(Q),_R:O.find_activeMenuList(Q),_V:D,_U:E,_q:F,_S:get_namaOPD(B),_T:c};return render(A,'account/popup.html',d)
@login_required(login_url=_O)
def komentar(request,mode='',pk='',photoID=''):
	B=mode;A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);G=_H;H=_H;photoID=[]
	if B==_G:
		if pk=='':return HttpResponse(_Y)
		I=crypt_uuid4.ClsCryptUuid4();F=I.dec_text(pk)
		if F=='':return HttpResponse(_Z)
		J=models.comment.objects.filter(site_id=C,id=F)
	if B==_G:
		for K in J:K.delete()
		return redirect('/dashboard/komentar')
	E='Comment';L=models.menu.objects.filter(nama=E,is_admin_menu=_B);M={_L:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:B,_U:G,_q:H,_S:get_namaOPD(C),_T:L};return render(A,'account/comment.html',M)
@login_required(login_url=_O)
def galery_layanan(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-layanan';J=photoID;D=mode;A=request;cek_user(A);C=get_siteID(A);L=menus.ClsMenus(C,_B);E=_H;F=_H;J=[]
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_layanan.objects.filter(site_id=C,id=M);W=models.galery_layanan.objects.filter(site_id=C,id=M)
		for B in W:J.append(B.photo.id)
	elif D==_N:I=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			E=forms.GaleryLayananForm(A.POST);F=I(A.POST);B=0
			for X in F:
				G=A.POST.get(_M+str(B)+_b);print('Galery Layanan = ');print(G)
				if G:
					if models.galery_layanan.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_v,A.POST.get(_F)));print('potential duplicate')
					else:print('else');N=A.POST.get(_M+str(B)+_c);O=save_photo_slideshow(B,C,N,G);print(_k+str(B));H=models.galery_layanan.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,photo_id=O.id);return redirect(Q)
				B+=1
		else:E=forms.GaleryLayananForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		S=get_object_or_404(R);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_J:
			E=forms.GaleryLayananForm(A.POST,instance=S);F=I(A.POST)
			if E.is_valid():
				H=E.save(commit=_C);H.site_id=C;H.admin_id=A.user.id;H.save();B=0
				for X in F:
					G=A.POST.get(_M+str(B)+_b)
					if G:N=A.POST.get(_M+str(B)+_c);O=save_photo_slideshow(B,C,N,G);print(_k+str(B));H.photo_id=O.id;H.save()
					B+=1
				messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(Q)
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
	P='galeri layanan';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_L:L.get_menus(),_Q:L.create_breadCrumb(P),_R:L.find_activeMenuList(P),_V:D,_U:E,_q:F,_S:get_namaOPD(C),_T:Y};return render(A,'account/galery-layanan.html',Z)
@login_required(login_url=_O)
def galery_video(request,mode='',pk='',photoID=''):
	I='/dashboard/galery-video';C=mode;A=request;cek_user(A);D=get_siteID(A);G=menus.ClsMenus(D,_B);B=_H;photoID=[]
	if C==_K or C==_G:
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
	elif C==_K:
		E=get_object_or_404(K)
		if A.method==_J:
			B=forms.GaleryVideoForm(A.POST,instance=E)
			if B.is_valid():F=B.save(commit=_C);F.site_id=D;F.admin_id=A.user.id;F.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(I)
		else:B=forms.GaleryVideoForm(instance=E,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:E=get_object_or_404(K);M=E.judul;E.delete();messages.info(A,mMsgBox.get(_G,M));return redirect(I)
	H='galeri video';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_L:G.get_menus(),_Q:G.create_breadCrumb(H),_R:G.find_activeMenuList(H),_V:C,_U:B,_S:get_namaOPD(D),_T:N};return render(A,'account/galery-video.html',O)
@login_required(login_url=_O)
def agenda(request,mode='',pk=''):
	H='/dashboard/agenda';D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);C=_H
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.agenda.objects.filter(site_id=E,id=I)
	if D==_N:
		if A.method==_J:
			C=forms.AgendaForm(A.POST,label_suffix='')
			if C.is_valid():
				B=C.save(commit=_C);B.site_id=E;B.admin_id=A.user.id
				if A.POST.get(_AH)!=''and A.POST.get('jam')!='':L=A.POST.get(_AH)+' '+A.POST.get('jam');B.waktu=datetime.strptime(L,'%d/%m/%Y %H:%M')
				B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		B=get_object_or_404(J)
		if A.method==_J:
			C=forms.AgendaForm(A.POST,A.FILES,instance=B,label_suffix='')
			if C.is_valid():O=C.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(H)
		else:C=forms.AgendaForm(instance=B,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:B=get_object_or_404(J);B.delete();messages.info(A,mMsgBox.get(_G,B.nama));return redirect(H)
	G='agenda';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:D,_U:C,_S:get_namaOPD(E),_T:M};return render(A,'account/agenda.html',N)
@login_required(login_url=_O)
def info_hoax(request,mode='',pk=''):
	H='/dashboard/info-hoax';C=mode;A=request;cek_user(A);E=get_siteID(A);print('siteID = ');print(E)
	if E!=1:messages.info(A,_AP);return redirect(_A8)
	F=menus.ClsMenus(E,_B);B=_H
	if C==_K or C==_G:
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
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_m)))
				return redirect(H)
		else:B=forms.InfoHoaxForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_K:
		D=get_object_or_404(J)
		if A.method==_J:
			B=forms.InfoHoaxForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_m)));return redirect(H)
		else:B=forms.InfoHoaxForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.name));return redirect(H)
	G='info hoaks';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_L:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(E),_T:M};return render(A,'account/info-hoax.html',N)
@login_required(login_url=_O)
def banner_all(request,mode='',pk='',photoID=''):
	T='/dashboard/banner-all';K=photoID;D=mode;A=request;cek_user(A);G=get_siteID(A)
	if G!=1:messages.info(A,_AP);return redirect(_A8)
	P=menus.ClsMenus(G,_B);B=_H;E=_H;K=[];H=''
	if D==_K or D==_G:
		if pk=='':return HttpResponse(_Y)
		Z=crypt_uuid4.ClsCryptUuid4();H=Z.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		U=models.banner_all.objects.filter(id=H);a=models.banner_all.objects.filter(id=H)
		for C in a:K.append(C.photo.id)
	elif D==_N:I=formset_factory(forms.PhotoForm)
	if D==_N:
		if A.method==_J:
			B=forms.BannerAllForm(A.POST);E=I(A.POST)
			if B.is_valid():
				print('form valid');C=0
				for b in E:
					J=A.POST.get(_M+str(C)+_b)
					if J:
						L=J.replace(_s,'');M=models.photo.Jenis.BANNER_ALL;N=models.photo.objects.create(site_id=G,jenis=M,file_path=L);Q=B.cleaned_data.get('site');F=B.save(commit=_C);F.photo_id=N.id;F.save()
						for R in Q:F.site.add(R)
					C+=1
			return redirect(T)
		else:B=forms.BannerAllForm(label_suffix='');E=I();messages.info(A,mMsgBox.get(_W))
	elif D==_K:
		V=get_object_or_404(U);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(K))
		if A.method==_J:
			B=forms.BannerAllForm(A.POST,instance=V);E=I(A.POST)
			if B.is_valid():
				Q=B.cleaned_data.get('site');models.banner_all.site.through.objects.filter(banner_all_id=H).delete();F=B.save();C=0
				for b in E:
					J=A.POST.get(_M+str(C)+_b)
					if J:
						L=J.replace(_s,'');M=models.photo.Jenis.BANNER_ALL;W=A.POST.get(_M+str(C)+_c)
						if W:N,c=models.photo.objects.update_or_create(id=W,defaults={_l:G,_r:M,_n:L})
						else:N,c=models.photo.objects.update_or_create(site_id=G,jenis=M,file_path=L)
						F.photo_id=N.id;F.save()
					C+=1
				for R in Q:F.site.add(R)
				messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(T)
		else:B=forms.BannerAllForm(instance=V,label_suffix='');E=I(queryset=models.photo.objects.filter(id__in=K));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		X=''
		for C in U:
			O=models.photo.objects.get(id=C.photo.id);X=C.name
			if O.file_path:
				if os.path.isfile(O.file_path.path):
					Y=Image.open(O.file_path.path)
					if Y:Y.close()
			O.delete()
		messages.info(A,mMsgBox.get(_G,X));return redirect(T)
	S='Banner All';d=models.menu.objects.filter(nama=S,is_admin_menu=_B);e={_L:P.get_menus(),_Q:P.create_breadCrumb(S),_R:P.find_activeMenuList(S),_V:D,_U:B,_q:E,_S:get_namaOPD(G),_T:d};return render(A,'account/banner-all.html',e)
def social_media_ajax(request):
	C=get_siteID(request);A=models.social_media.objects.filter(site_id=C).values(_A,_r,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def instansi_ajax(request):
	C=get_siteID(request);A=models.instansi.objects.filter(site_id=C).values(_A,_E,_A9,'telp',_A1,_AA,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def logo_ajax(request):
	C=get_siteID(request);A=models.logo.objects.filter(site_id=C).values(_A,'position',_t,_D).order_by('-updated_at')
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def banner_ajax(request):
	C=get_siteID(request);A=models.banner.objects.filter(site_id=C).values(_A,'position',_t,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_ajax(request):
	C=get_siteID(request);A=models.menu.objects.filter(site__id=C,is_admin_menu=_C,is_master_menu=_C).values(_A,_E,'href','icon',_u,_D).order_by(_o,_w)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_statis_ajax(request):A=get_siteID(request);B=models.menu.objects.filter(site__id=A,is_statis_menu=_B,is_admin_menu=_C).exclude(href='#').order_by(_o,_w);C=serializers.serialize('json',B,fields=(_A,_E));return HttpResponse(C,content_type='application/json')
def berita_ajax(request):
	C='photo__berita__id';D=get_siteID(request);E={'berita__id':OuterRef(C)};B=models.berita.objects.filter(site_id=D).values(_A,_F,_x,'kategori__nama',_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_x]=Truncator(A[_x]).chars(50)
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
	C='photo__pengumuman__id';D=get_siteID(request);E={'pengumuman__id':OuterRef(C)};B=models.pengumuman.objects.filter(site_id=D).values(_A,_F,_A4,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A4]=Truncator(A[_A4]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def artikel_ajax(request):
	C='photo__artikel__id';D=get_siteID(request);E={'artikel__id':OuterRef(C)};B=models.artikel.objects.filter(site_id=D).values(_A,_F,_A5,_e,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A5]=Truncator(A[_A5]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def dokumen_ajax(request):
	C='size';B=request;E=get_siteID(B);D=models.dokumen.objects.filter(site_id=E).values(_A,_E,_y,C,_n,_D)
	for A in D:A[_D]=get_natural_datetime(A[_D]);A[C]=naturalsize(A[C]);A[_n]=Truncator(A[_n]).chars(30);A['extra_field']='%s://%s%s%s'%(B.scheme,B.get_host(),settings.MEDIA_URL,A[_n])
	F=list(D);return JsonResponse(F,safe=_C)
def agenda_ajax(request):
	C=get_siteID(request);B=models.agenda.objects.filter(site_id=C).values(_A,_E,_y,'lokasi',_AH,'jam','penyelenggara','dihadiri_oleh',_e,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_y]=Truncator(A[_y]).words(30)
	D=list(B);return JsonResponse(D,safe=_C)
def pejabat_ajax(request,pIsDefault):
	C=get_siteID(request);A=models.pejabat.objects.filter(site__id=C,is_default=pIsDefault).values(_A,_E,_AG,_t,_D).order_by(_c)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def link_terkait_ajax(request):
	C=get_siteID(request);A=models.link_terkait.objects.filter(site__id=C).values(_A,_E,_j,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def halaman_statis_ajax(request):
	C='photo__halaman_statis__id';D=get_siteID(request);E={'halaman_statis__id':OuterRef(C)};B=models.halaman_statis.objects.filter(site_id=D).values(_A,_F,_z,'menu__nama',_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_z]=Truncator(A[_z]).chars(50)
	F=list(B);return JsonResponse(F,safe=_C)
def galery_foto_ajax(request):
	C=get_siteID(request);B=models.galery_foto.objects.filter(site_id=C).values(_A,_F,_t,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def popup_ajax(request):
	C=get_siteID(request);A=models.popup.objects.filter(site_id=C).values(_A,_F,_t,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def komentar_ajax(request):
	A='created_at';D=get_siteID(request);B=models.comment.objects.filter(site_id=D).values(_A,_m,_A1,'body','post__judul',A,'active')
	for C in B:C[A]=get_natural_datetime(C[A])
	E=list(B);return JsonResponse(E,safe=_C)
def galery_layanan_ajax(request):
	C=get_siteID(request);B=models.galery_layanan.objects.filter(site_id=C).values(_A,_F,_e,_t,_D)
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
	D=get_siteID(request);A=models.banner_all.objects.all().values(_A,_m,_j,_t,_e,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def enc_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.enc_text(data))
def dec_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.dec_text(data))
def toggle_comment_activate(request,pID):A=models.comment.objects.get(id=pID);A.active^=_B;A.save();return HttpResponse('True')
def toggle_comment_activate_all(request):A=models.comment.objects.filter(site_id=get_siteID(request),active=_C).update(active=_B);return HttpResponse('True')
def top_kontributor_berita(request):
	F=models.berita.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			print(_AQ)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_pengumuman(request):
	F=models.pengumuman.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			print(_AQ)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_artikel(request):
	F=models.artikel.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for(C,E)in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_i))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_i))+[0]);print('res = ');print(A)
	return JsonResponse(A,safe=_C)
def site_activity(request):
	D=[];G=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	for A in G:
		B=[];H=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for I in H:B.append(I[_A])
		J=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=B);C=len(B);E=J.filter(is_edited=_B).count()
		if C==0:F=0
		else:F=E/C*100
		K={_A:A[_A],_I:A[_I],_A7:C,_p:E,_A0:F};D.append(K)
	return JsonResponse(D,safe=_C)
def site_activity_pie_chart(request):
	C=[];P=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I));Q=0
	for A in P:
		D=[];R=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for S in R:D.append(S[_A])
		T=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=D);E=len(D);H=T.filter(is_edited=_B).count()
		if E==0:F=0
		else:F=H/E*100
		Q+=F;U={_A:A[_A],_I:A[_I],_A7:E,_p:H,_A0:F};C.append(U)
	C=sorted(C,key=lambda x:x[_A0],reverse=_B);B=[];I=10;J=0;K=0;L=0;M=0;G=_C;N=get_siteID(request);O=0
	for A in C:
		J+=1
		if J<I:
			B.append(A)
			if A[_A]==N:G=_B;print(_AK)
		elif len(B)<=I:
			if G:B.append(A);G=_C;print(_AL)
			elif A[_A]==N:B.append(A)
			else:K+=A[_p];L+=A[_A7];M+=A[_A0];O+=1
		else:K+=A[_p];L+=A[_A7];M+=A[_A0];O+=1
	return JsonResponse(B,safe=_C)
def site_activity_detail(request,siteID):
	B=siteID;C=[];H=[];F=list(models.menu.objects.filter(site__id=B,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AE,_w).values(_A,_E,_u))
	for A in F:
		D=models.halaman_statis.objects.filter(site__id=B,menu__id=A[_A],is_edited=_B)[:1]
		if D:
			for G in D:E={_A:A[_A],_o:A[_u],_L:A[_E],_F:G.judul,_p:1}
		else:E={_A:A[_A],_o:A[_u],_L:A[_E],_F:'',_p:0}
		C.append(E)
	return JsonResponse(C,safe=_C)
def site_activity_detail_pie_chart(request,siteID):
	F=siteID;B=[];L=[];I=list(models.menu.objects.filter(site__id=F,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AE,_w).values(_A,_E,_u))
	for A in I:
		G=models.halaman_statis.objects.filter(site__id=F,menu__id=A[_A],is_edited=_B)[:1]
		if G:
			for J in G:H={_A:A[_A],_o:A[_u],_L:A[_E],_F:J.judul,_p:1}
		else:H={_A:A[_A],_o:A[_u],_L:A[_E],_F:'',_p:0}
		B.append(H)
	print('begin create pie chart data');E=len(B);print(E);C=len(list(filter(lambda x:x[_p]==0,B)));print(C);D=len(list(filter(lambda x:x[_p]==1,B)));print(D);C=C/E*100;D=D/E*100;K=[{_m:'Menu Terisi','y':D,'sliced':_B,'selected':_B},{_m:'Menu Kosong','y':C}];return JsonResponse(K,safe=_C)
def site_productivity(request):
	B=[];F=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	for A in F:I=[];C=models.berita.objects.filter(site_id=A[_A]).count();D=models.artikel.objects.filter(site_id=A[_A]).count();E=models.pengumuman.objects.filter(site_id=A[_A]).count();G=C+D+E;H={_A:A[_A],_I:A[_I],_f:C,_g:E,_h:D,_d:G};B.append(H)
	B=sorted(B,key=lambda x:x[_d],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[]
	if J==1:L=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	else:
		S=list(models.instansi.objects.filter(kategori_id=J).values(_l))
		for A in S:K.append(A[_l])
		L=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_I).values(_A,_I))
	for A in L:W=[];M=models.berita.objects.filter(site_id=A[_A]).count();N=models.artikel.objects.filter(site_id=A[_A]).count();O=models.pengumuman.objects.filter(site_id=A[_A]).count();T=M+N+O;U={_A:A[_A],_I:A[_I],_f:M,_g:O,_h:N,_d:T};C.append(U)
	C=sorted(C,key=lambda x:x[_d],reverse=_B);B=[];P=10;Q=0;D=0;E=0;F=0;G=0;H=_C;R=get_siteID(request);I=0
	for A in C:
		Q+=1
		if Q<P:
			B.append(A)
			if A[_A]==R:H=_B;print(_AK)
		elif len(B)<=P:
			if H:B.append(A);H=_C;print(_AL)
			elif A[_A]==R:B.append(A)
			else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_d];I+=1
		else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_d];I+=1
	V={_A:0,_I:_AR+str(I)+_AS,_f:D,_g:E,_h:F,_d:G};B.append(V);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_table(request,kategori_id):
	C=kategori_id;B=[];D=[]
	if C==1:E=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	else:
		I=list(models.instansi.objects.filter(kategori_id=C).values(_l))
		for A in I:D.append(A[_l])
		E=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_I).values(_A,_I))
	for A in E:L=[];F=models.berita.objects.filter(site_id=A[_A]).count();G=models.artikel.objects.filter(site_id=A[_A]).count();H=models.pengumuman.objects.filter(site_id=A[_A]).count();J=F+G+H;K={_A:A[_A],_I:A[_I],_f:F,_g:H,_h:G,_d:J};B.append(K)
	B=sorted(B,key=lambda x:x[_d],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kualitas_table(request,kategori_id):
	B=kategori_id;C=[];D=[];E=100;J=50
	if B==1:F=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	else:
		K=list(models.instansi.objects.filter(kategori_id=B).values(_l))
		for A in K:D.append(A[_l])
		F=list(models.Site.objects.filter(id__in=D).exclude(id=1).order_by(_I).values(_A,_I))
	for A in F:N=[];G=models.berita.objects.filter(site_id=A[_A],word_count__gte=E).count();H=models.artikel.objects.filter(site_id=A[_A],word_count__gte=E).count();I=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=J).count();L=G+H+I;M={_A:A[_A],_I:A[_I],_f:G,_g:I,_h:H,_d:L};C.append(M)
	return JsonResponse(C,safe=_C)
def site_kontribusi_kualitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[];L=100;T=50
	if J==1:M=list(models.Site.objects.exclude(id=1).order_by(_I).values(_A,_I))
	else:
		U=list(models.instansi.objects.filter(kategori_id=J).values(_l))
		for A in U:K.append(A[_l])
		M=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_I).values(_A,_I))
	for A in M:Y=[];N=models.berita.objects.filter(site_id=A[_A],word_count__gte=L).count();O=models.artikel.objects.filter(site_id=A[_A],word_count__gte=L).count();P=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=T).count();V=N+O+P;W={_A:A[_A],_I:A[_I],_f:N,_g:P,_h:O,_d:V};C.append(W)
	C=sorted(C,key=lambda x:x[_d],reverse=_B);B=[];Q=10;R=0;D=0;E=0;F=0;G=0;H=_C;S=get_siteID(request);I=0
	for A in C:
		R+=1
		if R<Q:
			B.append(A)
			if A[_A]==S:H=_B;print(_AK)
		elif len(B)<=Q:
			if H:B.append(A);H=_C;print(_AL)
			elif A[_A]==S:B.append(A)
			else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_d];I+=1
		else:D+=A[_f];E+=A[_g];F+=A[_h];G+=A[_d];I+=1
	X={_A:0,_I:_AR+str(I)+_AS,_f:D,_g:E,_h:F,_d:G};B.append(X);return JsonResponse(B,safe=_C)
def site_ajax(request):
	A=request.GET.get('search')
	if A:B=models.Site.objects.filter(domain__icontains=A).exclude(id=1).values(_A,text=F(_I))
	else:B=models.Site.objects.exclude(id=1).values(_A,text=F(_I))
	return JsonResponse({'results':list(B),_AT:{'more':_B}},safe=_C)
def instansi_kategori_ajax(request):
	A=request.GET.get('search')
	if A:B=models.instansi_kategori.objects.filter(nama__icontains=A).values(_A,text=F(_E))
	else:B=models.instansi_kategori.objects.values(_A,text=F(_E))
	return JsonResponse({'results':list(B),_AT:{'more':_B}},safe=_C)