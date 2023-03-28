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
_A3='isi_berita'
_A2='/dashboard/menu'
_A1='photo'
_A0='email'
_z='persen'
_y='isi_halaman'
_x='order_menu'
_w='parent__nama'
_v='photo__file_path'
_u='site_id'
_t='media/'
_s='jenis'
_r='potential_duplicate_add'
_q='deskripsi'
_p='formset_img'
_o='file_path'
_n='terisi'
_m='parent'
_l='name'
_k='artikel'
_j='pengumuman'
_i='berita'
_h='total'
_g='save foto complete '
_f='link'
_e='username'
_d='status'
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
_N='domain'
_M='add'
_L='form-'
_K='menu'
_J='edit'
_I='POST'
_H=None
_G='delete'
_F='judul'
_E='nama'
_D='updated_at'
_C=False
_B=True
_A='id'
import base64,calendar,io,os
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.core import serializers
from django.core.files import File
from django.core.files.base import ContentFile
from django.db.models import Count,F,Min,OuterRef,Subquery
from django.forms import formset_factory,modelformset_factory
from django.http import Http404,JsonResponse
from django.shortcuts import HttpResponse,get_object_or_404,redirect,render
from django.utils.text import Truncator,slugify
from hitcount.models import Hit,HitCount
from humanize import intcomma,naturalsize
from PIL import Image
from account.commonf import get_topFoto
from account.forms import CustomUserCreationForm
from django_opd.commonf import get_natural_datetime
from opd import menus,models,views
from .  import crypt_uuid4,forms,msgbox
mMsgBox=msgbox.ClsMsgBox()
def redirect_to_login(request):
	if request.user.is_authenticated:return redirect(_A8)
	else:return redirect(_O)
def get_siteID(request):
	A=request;B=Site.objects.filter(domain=A.get_host()).values_list(_A,flat=_B)
	if B.count()==0:raise Http404("domain '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(A.get_host(),'/admin'))
	return B[0]
def get_namaOPD(pSiteID):
	A=Site.objects.filter(id=pSiteID).values_list(_l,flat=_B)[:1]
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
	B['bulan']=D;B[_i]=H;B[_j]=I;B[_k]=J;return B
def cek_user(request):
	A=request
	if not models.instansi.objects.filter(site_id=get_siteID(A),admin__id=A.user.id).exists():raise Http404("user <b>%s</b> tidak di temukan di domain <b>%s</b>. <a href='%s' onclick='%s'>Logout</a>"%(A.user.username,A.get_host(),'javascript:void(0)','login_again()'))
@login_required(login_url=_O)
def dashboard(request):A=request;cek_user(A);D=get_siteID(A);B=menus.ClsMenus(D,_B);E=get_hit_count(A);F=get_news_count(A);C='analytics';G=models.menu.objects.filter(nama=C,is_admin_menu=_B);H={_K:B.get_menus(),_Q:B.create_breadCrumb(C),_R:B.find_activeMenuList(C),_S:get_namaOPD(D),_T:G,_AM:E,_AN:F};return render(A,'account/dashboard.html',H)
@login_required(login_url=_O)
def dashboard_detail(request):
	G='text';B=request;cek_user(B);C=get_siteID(B);E=menus.ClsMenus(C,_B);I=models.berita.objects.exclude(site_id=1).count();J=models.artikel.objects.exclude(site_id=1).count();K=models.pengumuman.objects.exclude(site_id=1).count();H=models.Site.objects.get(id=C);L={_A:H.id,G:H.domain};D={};A=models.instansi.objects.filter(site_id=C)
	if A:
		A=A.get()
		if A.kategori:D={_A:A.kategori.id,G:A.kategori.nama}
	if not D:A=models.instansi_kategori.objects.get(id=1);D={_A:A.id,G:A.nama}
	print('form_data_kategori = ');print(D);M=get_hit_count(B);N=get_news_count(B);F='monitoring';O=models.menu.objects.filter(nama=F,is_admin_menu=_B);P={_K:E.get_menus(),_Q:E.create_breadCrumb(F),_R:E.find_activeMenuList(F),_S:get_namaOPD(C),_T:O,_AM:M,_AN:N,'mGrandTotal':I+K+J,'siteid':C,'form_data':L,'form_data_kategori':D};return render(B,'account/dashboard-detail.html',P)
def register(request):
	A=request
	if A.method==_I:
		B=CustomUserCreationForm(A.POST)
		if B.is_valid():C=B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_e)));return redirect(_O)
	else:B=forms.CustomUserCreationForm(label_suffix='')
	return render(A,'account/register.html',{_U:B})
@login_required(login_url=_O)
def social_media(request,mode='',pk=''):
	H='/dashboard/social-media';C=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_H
	if C==_J or C==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.social_media.objects.filter(site_id=E,id=I)
	if C==_M:
		if A.method==_I:
			B=forms.SocialMediaForm(A.POST,label_suffix='')
			if B.is_valid():
				if models.social_media.objects.filter(site_id=E,link=A.POST.get(_f)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_f)))
				else:
					L=models.social_media.objects.create(site_id=E,jenis=A.POST.get(_s),link=A.POST.get(_f))
					if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_s)))
					return redirect(H)
		else:B=forms.SocialMediaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_J:
		D=get_object_or_404(J)
		if A.method==_I:
			B=forms.SocialMediaForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_s)));return redirect(H)
		else:B=forms.SocialMediaForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.jenis));return redirect(H)
	G='social media';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(E),_T:M};return render(A,'account/social-media.html',N)
@login_required(login_url=_O)
def instansi(request,mode='',pk=''):
	I='/dashboard/instansi';C=mode;A=request;cek_user(A);D=get_siteID(A);E=menus.ClsMenus(D,_B);B=_H
	if C==_J:
		if pk=='':return HttpResponse(_Y)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		K=models.instansi.objects.filter(site_id=D,id=H)
	if C==_M:
		if A.method==_I:
			B=forms.InstansiForm(A.POST,label_suffix='')
			if B.is_valid():
				L=models.User.objects.get(id=A.user.id);M,N=models.instansi.objects.update_or_create(site_id=D,defaults={_E:A.POST.get(_E),_A9:A.POST.get(_A9),'telp':A.POST.get('telp'),_A0:A.POST.get(_A0),_AA:A.POST.get(_AA)});M.admin.add(L)
				if N:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect(I)
		else:B=forms.InstansiForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_J:
		F=get_object_or_404(K)
		if A.method==_I:
			B=forms.InstansiForm(A.POST,instance=F,label_suffix='')
			if B.is_valid():F.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(I)
		else:B=forms.InstansiForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	G='instansi';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:E.get_menus(),_Q:E.create_breadCrumb(G),_R:E.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(D),_T:O};return render(A,'account/instansi.html',P)
@login_required(login_url=_O)
def logo(request,mode='',pk=''):
	K='logo';J='Logo ';C='logo-position';A=request;cek_user(A);B=get_siteID(A);D=menus.ClsMenus(B,_B);E=_H;F=_H
	if mode==_M:
		if A.method==_I:
			E=forms.LogoForm(A.POST);F=forms.PhotoForm(A.POST)
			if A.POST.get(C).upper()=='TOP':H=models.photo.Jenis.LOGO_TOP
			else:H=models.photo.Jenis.LOGO_BOTTOM
			I=A.POST.get(_AB)
			if I:
				L=I.replace(_t,'');M,N=models.photo.objects.update_or_create(site_id=B,jenis=H,defaults={_o:L});Q,R=models.logo.objects.update_or_create(site_id=B,position=A.POST.get(C),defaults={_AC:M.id})
				if N:messages.info(A,mMsgBox.get(_X,J+A.POST.get(C)))
				else:messages.info(A,mMsgBox.get(_P,J+A.POST.get(C)))
			return redirect('/dashboard/logo')
		else:E=forms.LogoForm(label_suffix='',prefix=K);F=forms.PhotoForm(label_suffix='',prefix=_A1);messages.info(A,mMsgBox.get(_W))
	G=K;O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:D.get_menus(),_Q:D.create_breadCrumb(G),_R:D.find_activeMenuList(G),_V:mode,_U:E,_AD:F,_S:get_namaOPD(B),_T:O};return render(A,'account/logo.html',P)
@login_required(login_url=_O)
def banner(request,mode='',pk=''):
	K='banner';D='banner-position';A=request;cek_user(A);B=get_siteID(A);E=menus.ClsMenus(B,_B);F=_H;G=_H
	if mode==_M:
		if A.method==_I:
			F=forms.BannerForm(A.POST);G=forms.PhotoForm(A.POST);H=A.POST.get(D).upper()
			if H=='BOTTOM':C=models.photo.Jenis.BANNER_BOTTOM
			elif H=='MIDDLE1':C=models.photo.Jenis.BANNER_MIDDLE1
			elif H=='MIDDLE2':C=models.photo.Jenis.BANNER_MIDDLE2
			else:C=models.photo.Jenis.BANNER_TOP
			I=A.POST.get(_AB);print(_AO);print(I)
			if I:
				L=I.replace(_t,'');M,N=models.photo.objects.update_or_create(site_id=B,jenis=C,defaults={_o:L});Q,R=models.banner.objects.update_or_create(site_id=B,position=A.POST.get(D),defaults={_AC:M.id,_f:A.POST.get('banner-link')})
				if N:messages.info(A,mMsgBox.get(_X,A.POST.get(D)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(D)))
			return redirect('/dashboard/banner')
		else:F=forms.BannerForm(label_suffix='',prefix=K);G=forms.PhotoForm(label_suffix='',prefix=_A1);messages.info(A,mMsgBox.get(_W))
	J=K;O=models.menu.objects.filter(nama=J,is_admin_menu=_B);P={_K:E.get_menus(),_Q:E.create_breadCrumb(J),_R:E.find_activeMenuList(J),_V:mode,_U:F,_AD:G,_S:get_namaOPD(B),_T:O};return render(A,'account/banner.html',P)
def menu_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.menu.objects.filter(is_master_menu=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('menu_refresh'));return redirect(_A2)
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
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();M=W.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		N=models.menu.objects.filter(site__id=E,id=M)
	if D==_M or D==_m:
		if D==_m:F=pk
		if A.method==_I:
			C=forms.MenuForm(A.POST,label_suffix='')
			if C.is_valid():
				G=models.Site.objects.get(id=E);F=A.POST.get(_m)
				if not F:F=_H
				O=_B;P=models.menu.objects.filter(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F).values_list(S,flat=_B)
				if P.count()>0:
					if P[0]==_B:messages.info(A,mMsgBox.get(T));C=forms.MenuForm(label_suffix='');O=_C
				if O:
					X,Y=models.menu.objects.update_or_create(site__id=G.id,nama__iexact=A.POST.get(_E),parent_id=F,defaults={_E:A.POST.get(_E),'href':'menu/'+slugify(A.POST.get(_E)),'icon':A.POST.get('icon'),_x:A.POST.get(_x),'is_visibled':_B,'is_statis_menu':_B});X.site.add(G)
					if Y:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
					return redirect(_A2)
		else:C=forms.MenuForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		B=get_object_or_404(N)
		if A.method==_I:
			C=forms.MenuForm(A.POST,instance=B,label_suffix='')
			if A.POST.get(_m)==str(B.id):messages.info(A,mMsgBox.get('circular_menu'));C=forms.MenuForm(instance=B,label_suffix='')
			elif A.POST.get(S):messages.info(A,mMsgBox.get(T));C=forms.MenuForm(instance=B,label_suffix='')
			elif C.is_valid():B=C.save(commit=_C);B.is_statis_menu=1;B.is_visibled=1;B.save();G=models.Site.objects.get(id=E);B.site.add(G);messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(_A2)
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
		return redirect(_A2)
	K=_K;b=models.menu.objects.filter(nama=K,is_admin_menu=_B);c={_K:J.get_menus(),_Q:J.create_breadCrumb(K),_R:J.find_activeMenuList(K),_V:D,_U:C,'menu_master':L,_AE:F,_S:get_namaOPD(E),_T:b};return render(A,'account/menu.html',c)
def delete_photo(request):
	print('inside delete photo');C=range(3)
	for B in C:
		A=request.POST.get('file_path_'+str(B));print(A)
		if A!='':
			if os.path.isfile(A):os.remove(A);print('remove photo success '+str(B))
	return HttpResponse('OKE')
def upload_photo(request,width,height):
	S='JPEG';R='RGBA';Q='image/png';P='.jpeg';K=height;J=width;I='/';H=request;print('inside upload photo');print(J);print(K);print('result = ');A=H.FILES.get(_A1);print(A);F=H.POST.get('old_photo');print('Old Photo = ');print(F)
	if F:
		if os.path.isfile(F):os.remove(F);print('remove photo success')
	print(A.size);print('Content TYPE = ');print(A.content_type);T=get_siteID(H);L=Image.open(io.BytesIO(A.read()));print('image');print(L);B=L.resize((J,K),Image.ANTIALIAS);print('resized_image');print(B);G=datetime.now();M=str(T)+'-'+G.strftime('%Y%m%d-%H%M%S-%f');print('filename');print(M);U=G.strftime('%Y');V=G.strftime('%m');W=G.strftime('%d')
	if A.content_type=='image/gif':C='.gif'
	elif A.content_type=='image/jpeg':C=P
	elif A.content_type=='image/jpg':C='.jpg'
	elif A.content_type==Q:C=P
	elif A.content_type=='image/bmp':C='.bmp'
	else:C='.ief'
	print('ext');print(C);X=settings.BASE_DIR;N=settings.MEDIA_ROOT;print('base_dir');print(X);D='crop/'+U+I+V+I+W+I;print('path');print(D);E=os.path.join(N,D);Y=os.makedirs(E,exist_ok=_B);print('makedirs');print(Y);D=D+M+C;E=os.path.join(N,D)
	if A.content_type==Q:
		B.load();O=Image.new('RGB',B.size,(255,255,255));print('Image PNG ')
		if B.mode==R:print(R);O.paste(B,mask=B.getchannel('A'));O.save(E,S,quality=80,optimize=_B)
		else:print('NON RGBA');B.save(E,S,quality=80,optimize=_B)
	else:print('NON PNG');B.save(E,quality=80,optimize=_B)
	print('resize image');return HttpResponse(D)
def get_photo_kind(idx):
	B=idx;A=_H
	if B==0:A=models.photo.Jenis.HIGHLIGHT1
	elif B==1:A=models.photo.Jenis.HIGHLIGHT2
	elif B==2:A=models.photo.Jenis.HIGHLIGHT3
	return A
def save_photo_slideshow(idx,site_id,photo_id,str_foto_path):
	C=photo_id;B=site_id;print('Begin INSPECT');D=get_photo_kind(idx);print('mode add/edit PHOTO IDs == ');print(C);E=str_foto_path;print('str_foto_path_replace');print(E);print(_s);print(D);print('siteid');print(B)
	if C:A=models.photo.objects.get(id=C);A.site_id=B;A.jenis=D;A.file_path=E;A.save();print('[save_photo_slideshow] - Update foto complete')
	else:A=models.photo.objects.create(site_id=B,jenis=D,file_path=E);print('[save_photo_slideshow] - save foto complete')
	print('END INSPECT');return A
def save_tags(tag_list,obj_master):
	B=obj_master;A=tag_list;print('id berita = ');print(B.id);print('tag list = ');print(A);models.berita.tags.through.objects.filter(berita_id=B.id).delete();C=0
	while C<len(A):D=models.tags.objects.get(id=A[C]);B.tags.add(D);C+=1
@login_required(login_url=_O)
def berita(request,mode='',pk='',photoID=''):
	U='/dashboard/berita';M=photoID;D=mode;A=request;cek_user(A);C=get_siteID(A);O=menus.ClsMenus(C,_B);E=_H;F=_H;M=[]
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		X=crypt_uuid4.ClsCryptUuid4();N=X.dec_text(pk)
		if N=='':return HttpResponse(_Z)
		V=models.berita.objects.filter(site_id=C,id=N);P=models.berita.photo.through.objects.filter(berita__site=C,berita__id=N)
		for B in P:M.append(B.photo.id)
	elif D==_M:H=formset_factory(forms.PhotoForm,extra=3)
	if D==_M:
		if A.method==_I:
			E=forms.BeritaForm(A.POST);F=H(A.POST)
			if models.berita.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_F)))
			else:
				Q=models.berita.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,kategori_id=A.POST.get('kategori'),isi_berita=A.POST.get(_A3),status=A.POST.get(_d));R=A.POST.getlist('tags');save_tags(R,Q);B=0
				for Y in F:
					G=A.POST.get(_L+str(B)+_b)
					if G:
						S=A.POST.get(_L+str(B)+_c);I=save_photo_slideshow(B,C,S,G);print('obj_photo = ');print(I)
						if I:Q.photo.add(I);print(_g+str(B))
					B+=1
				if Q:messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
				return redirect(U)
		else:E=forms.BeritaForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		J=get_object_or_404(V);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(M))
		if A.method==_I:
			E=forms.BeritaForm(A.POST,instance=J);F=H(A.POST);print('MODE EDIT, POST')
			if E.is_valid():
				print('FORM VALID');K=E.save(commit=_C);K.site_id=C;K.admin_id=A.user.id;K.save();print('SAVE COMPLETE');R=A.POST.getlist('tags');save_tags(R,K);print('save tag complete');B=0
				for Y in F:
					G=A.POST.get(_L+str(B)+_b);print('str_foto_path');print(G)
					if G!='':S=A.POST.get(_L+str(B)+_c);I=save_photo_slideshow(B,C,S,G);K.photo.add(I);print(_g+str(B))
					B+=1
				messages.info(A,mMsgBox.get(_P,'Berita'));return redirect(U)
		else:E=forms.BeritaForm(instance=J,label_suffix='');F=H(queryset=models.photo.objects.filter(id__in=M));messages.info(A,mMsgBox.get(_a))
	elif D==_G:
		for B in P:
			L=models.photo.objects.get(id=B.photo.id)
			if L.file_path:
				print('obj_img.file_path = ');print(L.file_path)
				if os.path.exists(L.file_path.path):
					W=Image.open(L.file_path.path)
					if W:W.close()
			L.delete()
		P=models.berita.photo.through.objects.filter(berita__site=C,berita__id=N).delete();J=get_object_or_404(V);J.delete();messages.info(A,mMsgBox.get(_G,J.judul));return redirect(U)
	T=_i;Z=models.menu.objects.filter(nama=T,is_admin_menu=_B);a={_K:O.get_menus(),_Q:O.create_breadCrumb(T),_R:O.find_activeMenuList(T),_V:D,_U:E,_p:F,_S:get_namaOPD(C),_T:Z};return render(A,'account/berita.html',a)
@login_required(login_url=_O)
def kategori(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_H
	if mode==_M:
		if A.method==_I:
			B=forms.KategoriForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.kategori.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect('/dashboard/kategori')
		else:B=forms.KategoriForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='kategori';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:mode,_U:B,_S:get_namaOPD(C),_T:I};return render(A,'account/kategori.html',J)
@login_required(login_url=_O)
def tags(request,mode='',pk=''):
	A=request;cek_user(A);C=get_siteID(A);D=menus.ClsMenus(C,_B);B=_H
	if mode==_M:
		if A.method==_I:
			B=forms.TagsForm(A.POST,label_suffix='')
			if B.is_valid():
				F=models.Site.objects.get(id=C);G,H=models.tags.objects.get_or_create(nama__iexact=A.POST.get(_E),defaults={_E:A.POST.get(_E)});G.site.add(F)
				if H:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect('/dashboard/tags')
		else:B=forms.TagsForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	E='tags';I=models.menu.objects.filter(nama=E,is_admin_menu=_B);J={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:mode,_U:B,_S:get_namaOPD(C),_T:I};return render(A,'account/tags.html',J)
@login_required(login_url=_O)
def pengumuman(request,mode='',pk=''):
	W='Pengumuman';S='/dashboard/pengumuman';D=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);E=_H;F=_H;N=[]
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		X=crypt_uuid4.ClsCryptUuid4();J=X.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		T=models.pengumuman.objects.filter(site_id=C,id=J);O=models.pengumuman.photo.through.objects.filter(pengumuman__site=C,pengumuman__id=J)
		for B in O:N.append(B.photo.id)
	elif D==_M:G=formset_factory(forms.PhotoForm,extra=3)
	if D==_M:
		if A.method==_I:
			E=forms.PengumumanForm(A.POST);F=G(A.POST)
			if models.pengumuman.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_F)))
			else:
				U=models.pengumuman.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_pengumuman=A.POST.get(_A4),status=A.POST.get(_d));B=0
				for Y in F:
					H=A.POST.get(_L+str(B)+_b)
					if H:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);U.photo.add(Q);print(_g+str(B))
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,W))
				return redirect(S)
		else:E=forms.PengumumanForm(label_suffix='');F=G();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		I=get_object_or_404(T);G=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_I:
			E=forms.PengumumanForm(A.POST,instance=I);F=G(A.POST)
			if E.is_valid():
				K=E.save(commit=_C);K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for Y in F:
					H=A.POST.get(_L+str(B)+_b)
					if H:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);K.photo.add(Q);print(_g+str(B))
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
	R=_j;Z=models.menu.objects.filter(nama=R,is_admin_menu=_B);a={_K:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:D,_U:E,_p:F,_S:get_namaOPD(C),_T:Z};return render(A,'account/pengumuman.html',a)
@login_required(login_url=_O)
def artikel(request,mode='',pk=''):
	S='/dashboard/artikel';D=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);E=_H;F=_H;N=[]
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		W=crypt_uuid4.ClsCryptUuid4();J=W.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		T=models.artikel.objects.filter(site_id=C,id=J);O=models.artikel.photo.through.objects.filter(artikel__site=C,artikel__id=J)
		for B in O:N.append(B.photo.id)
	elif D==_M:G=formset_factory(forms.PhotoForm,extra=3)
	if D==_M:
		if A.method==_I:
			E=forms.ArtikelForm(A.POST);F=G(A.POST)
			if models.artikel.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_F)))
			else:
				U=models.artikel.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,isi_artikel=A.POST.get(_A5),status=A.POST.get(_d));B=0
				for X in F:
					H=A.POST.get(_L+str(B)+_b)
					if H:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);U.photo.add(Q);print(_g+str(B))
					B+=1
				if U:messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
				return redirect(S)
		else:E=forms.ArtikelForm(label_suffix='');F=G();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		I=get_object_or_404(T);G=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_I:
			E=forms.ArtikelForm(A.POST,instance=I);F=G(A.POST)
			if E.is_valid():
				K=E.save(commit=_C);K.site_id=C;K.admin_id=A.user.id;K.save();B=0
				for X in F:
					H=A.POST.get(_L+str(B)+_b)
					if H:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,H);K.photo.add(Q);print(_g+str(B))
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
	R=_k;Y=models.menu.objects.filter(nama=R,is_admin_menu=_B);Z={_K:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:D,_U:E,_p:F,_S:get_namaOPD(C),_T:Y};return render(A,'account/artikel.html',Z)
def pejabat_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.pejabat.objects.filter(is_default=_B)
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('pejabat_refresh'));return redirect(_AF)
@login_required(login_url=_O)
def pejabat(request,mode='',pk=''):
	C=mode;A=request;cek_user(A);B=get_siteID(A);E=menus.ClsMenus(B,_B);F=_H;G=_H
	if C==_J or C==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		M=models.pejabat.objects.filter(site__id=B,id=J)
	if C==_M:
		if A.method==_I:
			F=forms.PejabatForm(A.POST);G=forms.PhotoForm(A.POST);N=models.photo.Jenis.PEJABAT_OPD;K=A.POST.get(_AB)
			if K:
				O=K.replace(_t,'');P,Q=models.photo.objects.update_or_create(site_id=B,jenis=N,defaults={_o:O});R,V=models.pejabat.objects.update_or_create(site__id=B,jabatan_index=models.pejabat.Position.PEJABAT_OPD,defaults={_AC:P.id,_E:A.POST.get(_E),_AG:A.POST.get(_AG),'admin_id':A.user.id,'is_default':0});S=models.Site.objects.get(id=B);R.site.add(S)
				if Q:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
			return redirect(_AF)
		else:F=forms.PejabatForm(label_suffix='');G=forms.PhotoForm(label_suffix='',prefix=_A1);messages.info(A,mMsgBox.get(_W))
	elif C==_G:
		D=get_object_or_404(M);print('post = ');print(D.photo.id);H=models.photo.objects.filter(id=D.photo.id);print('foto = ');print(H)
		if H:H.delete()
		D.delete();messages.info(A,mMsgBox.get(_G,D.nama));return redirect(_AF)
	I='pejabat';T=models.menu.objects.filter(nama=I,is_admin_menu=_B);U={_K:E.get_menus(),_Q:E.create_breadCrumb(I),_R:E.find_activeMenuList(I),_V:C,_U:F,_AD:G,_S:get_namaOPD(B),_T:T};return render(A,'account/pejabat.html',U)
def link_terkait_refresh(request):
	A=request;B=models.Site.objects.get(id=get_siteID(A));C=models.link_terkait.objects.all()
	for D in C:D.site.add(B)
	messages.info(A,mMsgBox.get('link_terkait_refresh'));return redirect(_A6)
@login_required(login_url=_O)
def link_terkait(request,mode='',pk=''):
	D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);B=_H
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		J=crypt_uuid4.ClsCryptUuid4();H=J.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		I=models.link_terkait.objects.filter(site__id=E,id=H)
	if D==_M:
		if A.method==_I:
			B=forms.LinkTerkaitForm(A.POST,label_suffix='')
			if B.is_valid():
				K,L=models.link_terkait.objects.update_or_create(site__id=E,nama=A.POST.get(_E),defaults={_f:A.POST.get(_f)});M=models.Site.objects.get(id=E);K.site.add(M)
				if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
				return redirect(_A6)
		else:B=forms.LinkTerkaitForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		C=get_object_or_404(I)
		if A.method==_I:
			B=forms.LinkTerkaitForm(A.POST,instance=C,label_suffix='')
			if B.is_valid():C.save();N=models.Site.objects.get(id=E);C.site.add(N);messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(_A6)
		else:B=forms.LinkTerkaitForm(instance=C,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:C=get_object_or_404(I);C.delete();messages.info(A,mMsgBox.get(_G,C.nama));return redirect(_A6)
	G='link terkait';O=models.menu.objects.filter(nama=G,is_admin_menu=_B);P={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:D,_U:B,_S:get_namaOPD(E),_T:O};return render(A,'account/link-terkait.html',P)
@login_required(login_url=_O)
def dokumen(request,mode='',pk=''):
	I='/dashboard/dokumen';D=mode;A=request;cek_user(A);E=get_siteID(A);G=menus.ClsMenus(E,_B);B=_H
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		K=models.dokumen.objects.filter(site_id=E,id=J)
	if D==_M:
		if A.method==_I:
			B=forms.DokumenForm(A.POST,A.FILES,label_suffix='')
			if B.is_valid():
				M=A.FILES.get(_o)
				if models.dokumen.objects.filter(site_id=E,nama__iexact=A.POST.get(_E)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_E)))
				else:
					C=models.dokumen.objects.create(site_id=E,nama=A.POST.get(_E),admin_id=A.user.id,file_path=M,deskripsi=A.POST.get(_q),status=A.POST.get(_d));C.size=os.stat(C.file_path.path).st_size;C.save()
					if C:messages.info(A,mMsgBox.get(_X,A.POST.get(_E)))
					return redirect(I)
		else:B=forms.DokumenForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		F=get_object_or_404(K)
		if A.method==_I:
			B=forms.DokumenForm(A.POST,A.FILES,instance=F,label_suffix='')
			if B.is_valid():C=B.save();C.size=os.stat(C.file_path.path).st_size;C.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_E)));return redirect(I)
		else:B=forms.DokumenForm(instance=F,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif D==_G:F=get_object_or_404(K);F.delete();messages.info(A,mMsgBox.get(_G,F.nama));return redirect(I)
	H='dokumen';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_K:G.get_menus(),_Q:G.create_breadCrumb(H),_R:G.find_activeMenuList(H),_V:D,_U:B,_S:get_namaOPD(E),_T:N};return render(A,'account/dokumen.html',O)
@login_required(login_url=_O)
def halaman_statis(request,mode='',pk=''):
	S='/dashboard/halaman-statis';E=mode;A=request;cek_user(A);C=get_siteID(A);M=menus.ClsMenus(C,_B);D=_H;F=_H;N=[]
	if E==_J or E==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();K=V.dec_text(pk)
		if K=='':return HttpResponse(_Z)
		T=models.halaman_statis.objects.filter(site_id=C,id=K);O=models.halaman_statis.photo.through.objects.filter(halaman_statis__site=C,halaman_statis__id=K)
		for B in O:N.append(B.photo.id)
	elif E==_M:H=formset_factory(forms.PhotoForm,extra=3)
	if E==_M:
		if A.method==_I:
			D=forms.HalamanStatisForm(A.POST);F=H(A.POST)
			if D.is_valid():
				if models.halaman_statis.objects.filter(site_id=C,menu_id=A.POST.get(_K)).count()>1:messages.info(A,mMsgBox.get('menu_already_exists'))
				else:
					G,Z=models.halaman_statis.objects.update_or_create(site_id=C,menu_id=A.POST.get(_K),defaults={_u:C,_F:A.POST.get(_F),_y:A.POST.get(_y),'admin_id':A.user.id,'is_edited':_B});B=0
					for W in F:
						I=A.POST.get(_L+str(B)+_b)
						if I:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,I);G.photo.add(Q);print(_g+str(B))
						B+=1
					messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(S)
		else:D=forms.HalamanStatisForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif E==_J:
		J=get_object_or_404(T);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=3-len(N))
		if A.method==_I:
			D=forms.HalamanStatisForm(A.POST,instance=J);F=H(A.POST)
			if D.is_valid():
				G=D.save(commit=_C);G.site_id=C;G.admin_id=A.user.id;G.is_edited=_B;G.save();B=0
				for W in F:
					I=A.POST.get(_L+str(B)+_b)
					if I:P=A.POST.get(_L+str(B)+_c);Q=save_photo_slideshow(B,C,P,I);G.photo.add(Q);print(_g+str(B))
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
	R='halaman statis';X=models.menu.objects.filter(nama=R,is_admin_menu=_B);Y={_K:M.get_menus(),_Q:M.create_breadCrumb(R),_R:M.find_activeMenuList(R),_V:E,_U:D,_p:F,_S:get_namaOPD(C),_T:X};return render(A,'account/halaman-statis.html',Y)
@login_required(login_url=_O)
def galery_foto(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-foto';J=photoID;C=mode;A=request;cek_user(A);D=get_siteID(A);L=menus.ClsMenus(D,_B);E=_H;F=_H;J=[];print('mode = ');print(C)
	if C==_J or C==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_foto.objects.filter(site_id=D,id=M);W=models.galery_foto.objects.filter(site_id=D,id=M)
		for B in W:J.append(B.photo.id)
	elif C==_M:H=formset_factory(forms.PhotoForm)
	if C==_M:
		if A.method==_I:
			E=forms.GaleryFotoForm(A.POST);F=H(A.POST);B=0
			for X in F:
				G=A.POST.get(_L+str(B)+_b);print(_AO);print(G)
				if G:N=A.POST.get(_L+str(B)+_c);O=save_photo_slideshow(B,D,N,G);print(_g+str(B));a=models.galery_foto.objects.create(site_id=D,judul=A.POST.get(_F),admin_id=A.user.id,deskripsi=A.POST.get(_q),photo_id=O.id)
				B+=1
			return redirect(Q)
		else:E=forms.GaleryFotoForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif C==_J:
		S=get_object_or_404(R);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_I:
			E=forms.GaleryFotoForm(A.POST,instance=S);F=H(A.POST)
			if E.is_valid():
				print('yes form is valid');I=E.save(commit=_C);I.site_id=D;I.admin_id=A.user.id;I.save();B=0
				for X in F:
					G=A.POST.get(_L+str(B)+_b)
					if G:N=A.POST.get(_L+str(B)+_c);O=save_photo_slideshow(B,D,N,G);print(_g+str(B));I.photo_id=O.id;I.save()
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
	P='galeri foto';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_K:L.get_menus(),_Q:L.create_breadCrumb(P),_R:L.find_activeMenuList(P),_V:C,_U:E,_p:F,_S:get_namaOPD(D),_T:Y};return render(A,'account/galery-foto.html',Z)
@login_required(login_url=_O)
def popup(request,mode='',pk='',photoID=''):
	X='published';R='/dashboard/popup';J=photoID;D=mode;A=request;cek_user(A);B=get_siteID(A);O=menus.ClsMenus(B,_B);E=_H;F=_H;J=[]
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		Y=crypt_uuid4.ClsCryptUuid4();P=Y.dec_text(pk)
		if P=='':return HttpResponse(_Z)
		S=models.popup.objects.filter(site_id=B,id=P);Z=models.popup.objects.filter(site_id=B,id=P)
		for C in Z:J.append(C.photo.id)
	elif D==_M:H=formset_factory(forms.PhotoForm)
	if D==_M:
		if A.method==_I:
			E=forms.PopupForm(A.POST);F=H(A.POST);C=0
			for a in F:
				I=A.POST.get(_L+str(C)+_b)
				if I:
					K=I.replace(_t,'');L=models.photo.Jenis.POPUP
					if A.POST.get(_d)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
					if models.popup.objects.filter(site_id=B,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_F)))
					else:M=models.photo.objects.create(site_id=B,jenis=L,file_path=K);G=models.popup.objects.create(site_id=B,judul=A.POST.get(_F),admin_id=A.user.id,status=A.POST.get(_d),photo_id=M.id)
				C+=1
			return redirect(R)
		else:E=forms.PopupForm(label_suffix='');F=H();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		T=get_object_or_404(S);H=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_I:
			E=forms.PopupForm(A.POST,instance=T);F=H(A.POST)
			if E.is_valid():
				if A.POST.get(_d)==X:models.popup.objects.filter(site_id=B,status=models.Status.PUBLISHED).update(status=models.Status.DRAFT)
				G=E.save(commit=_C);G.site_id=B;G.admin_id=A.user.id;G.save();C=0
				for a in F:
					I=A.POST.get(_L+str(C)+_b)
					if I:
						K=I.replace(_t,'');L=models.photo.Jenis.POPUP;U=A.POST.get(_L+str(C)+_c)
						if U:M,b=models.photo.objects.update_or_create(id=U,defaults={_u:B,_s:L,_o:K})
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
	Q='Popup';c=models.menu.objects.filter(nama=Q,is_admin_menu=_B);d={_K:O.get_menus(),_Q:O.create_breadCrumb(Q),_R:O.find_activeMenuList(Q),_V:D,_U:E,_p:F,_S:get_namaOPD(B),_T:c};return render(A,'account/popup.html',d)
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
	E='Comment';L=models.menu.objects.filter(nama=E,is_admin_menu=_B);M={_K:D.get_menus(),_Q:D.create_breadCrumb(E),_R:D.find_activeMenuList(E),_V:B,_U:G,_p:H,_S:get_namaOPD(C),_T:L};return render(A,'account/comment.html',M)
@login_required(login_url=_O)
def galery_layanan(request,mode='',pk='',photoID=''):
	Q='/dashboard/galery-layanan';J=photoID;D=mode;A=request;cek_user(A);C=get_siteID(A);L=menus.ClsMenus(C,_B);E=_H;F=_H;J=[]
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		V=crypt_uuid4.ClsCryptUuid4();M=V.dec_text(pk)
		if M=='':return HttpResponse(_Z)
		R=models.galery_layanan.objects.filter(site_id=C,id=M);W=models.galery_layanan.objects.filter(site_id=C,id=M)
		for B in W:J.append(B.photo.id)
	elif D==_M:I=formset_factory(forms.PhotoForm)
	if D==_M:
		if A.method==_I:
			E=forms.GaleryLayananForm(A.POST);F=I(A.POST);B=0
			for X in F:
				G=A.POST.get(_L+str(B)+_b);print('Galery Layanan = ');print(G)
				if G:
					if models.galery_layanan.objects.filter(site_id=C,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_r,A.POST.get(_F)));print('potential duplicate')
					else:print('else');N=A.POST.get(_L+str(B)+_c);O=save_photo_slideshow(B,C,N,G);print(_g+str(B));H=models.galery_layanan.objects.create(site_id=C,judul=A.POST.get(_F),admin_id=A.user.id,photo_id=O.id);return redirect(Q)
				B+=1
		else:E=forms.GaleryLayananForm(label_suffix='');F=I();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		S=get_object_or_404(R);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(J))
		if A.method==_I:
			E=forms.GaleryLayananForm(A.POST,instance=S);F=I(A.POST)
			if E.is_valid():
				H=E.save(commit=_C);H.site_id=C;H.admin_id=A.user.id;H.save();B=0
				for X in F:
					G=A.POST.get(_L+str(B)+_b)
					if G:N=A.POST.get(_L+str(B)+_c);O=save_photo_slideshow(B,C,N,G);print(_g+str(B));H.photo_id=O.id;H.save()
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
	P='galeri layanan';Y=models.menu.objects.filter(nama=P,is_admin_menu=_B);Z={_K:L.get_menus(),_Q:L.create_breadCrumb(P),_R:L.find_activeMenuList(P),_V:D,_U:E,_p:F,_S:get_namaOPD(C),_T:Y};return render(A,'account/galery-layanan.html',Z)
@login_required(login_url=_O)
def galery_video(request,mode='',pk='',photoID=''):
	I='/dashboard/galery-video';C=mode;A=request;cek_user(A);D=get_siteID(A);G=menus.ClsMenus(D,_B);B=_H;photoID=[]
	if C==_J or C==_G:
		if pk=='':return HttpResponse(_Y)
		L=crypt_uuid4.ClsCryptUuid4();J=L.dec_text(pk)
		if J=='':return HttpResponse(_Z)
		K=models.galery_video.objects.filter(site_id=D,id=J)
	if C==_M:
		if A.method==_I:
			B=forms.GaleryVideoForm(A.POST)
			if models.galery_video.objects.filter(site_id=D,judul__iexact=A.POST.get(_F)).exists():messages.info(A,mMsgBox.get(_X,A.POST.get(_F)))
			else:F=models.galery_video.objects.create(site_id=D,judul=A.POST.get(_F),admin_id=A.user.id,embed=A.POST.get('embed'));return redirect(I)
		else:B=forms.GaleryVideoForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_J:
		E=get_object_or_404(K)
		if A.method==_I:
			B=forms.GaleryVideoForm(A.POST,instance=E)
			if B.is_valid():F=B.save(commit=_C);F.site_id=D;F.admin_id=A.user.id;F.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_F)));return redirect(I)
		else:B=forms.GaleryVideoForm(instance=E,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:E=get_object_or_404(K);M=E.judul;E.delete();messages.info(A,mMsgBox.get(_G,M));return redirect(I)
	H='galeri video';N=models.menu.objects.filter(nama=H,is_admin_menu=_B);O={_K:G.get_menus(),_Q:G.create_breadCrumb(H),_R:G.find_activeMenuList(H),_V:C,_U:B,_S:get_namaOPD(D),_T:N};return render(A,'account/galery-video.html',O)
@login_required(login_url=_O)
def agenda(request,mode='',pk=''):
	J='/dashboard/agenda';D=mode;A=request;cek_user(A);E=get_siteID(A);F=menus.ClsMenus(E,_B);C=_H
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();H=K.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		I=models.agenda.objects.filter(site_id=E,id=H)
	if D==_M:
		if A.method==_I:
			C=forms.AgendaForm(A.POST,label_suffix='')
			if C.is_valid():
				B=C.save(commit=_C);B.site_id=E;B.admin_id=A.user.id
				if A.POST.get(_AH)!=''and A.POST.get('jam')!='':L=A.POST.get(_AH)+' '+A.POST.get('jam');B.waktu=datetime.strptime(L,'%d/%m/%Y %H:%M')
				B.save();messages.info(A,mMsgBox.get(_X,A.POST.get(_E)));return redirect(J)
		else:C=forms.AgendaForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		B=get_object_or_404(I)
		if A.method==_I:
			C=forms.AgendaForm(A.POST,A.FILES,instance=B,label_suffix='')
			if C.is_valid():O=C.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_E)))
			messages.info(A,mMsgBox.get(_a))
	elif D==_G:B=get_object_or_404(I);B.delete();messages.info(A,mMsgBox.get(_G,B.nama));return redirect(J)
	G='agenda';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:D,_U:C,_S:get_namaOPD(E),_T:M};return render(A,'account/agenda.html',N)
@login_required(login_url=_O)
def info_hoax(request,mode='',pk=''):
	H='/dashboard/info-hoax';C=mode;A=request;cek_user(A);E=get_siteID(A);print('siteID = ');print(E)
	if E!=1:messages.info(A,_AP);return redirect(_A8)
	F=menus.ClsMenus(E,_B);B=_H
	if C==_J or C==_G:
		if pk=='':return HttpResponse(_Y)
		K=crypt_uuid4.ClsCryptUuid4();I=K.dec_text(pk)
		if I=='':return HttpResponse(_Z)
		J=models.info_hoax.objects.filter(id=I)
	if C==_M:
		if A.method==_I:
			B=forms.InfoHoaxForm(A.POST,label_suffix='')
			if B.is_valid():
				O,L=models.info_hoax.objects.update_or_create(name=A.POST.get(_l),defaults={_f:A.POST.get(_f)})
				if L:messages.info(A,mMsgBox.get(_X,A.POST.get(_l)))
				else:messages.info(A,mMsgBox.get(_P,A.POST.get(_l)))
				return redirect(H)
		else:B=forms.InfoHoaxForm(label_suffix='');messages.info(A,mMsgBox.get(_W))
	elif C==_J:
		D=get_object_or_404(J)
		if A.method==_I:
			B=forms.InfoHoaxForm(A.POST,instance=D,label_suffix='')
			if B.is_valid():D.save();messages.info(A,mMsgBox.get(_P,A.POST.get(_l)));return redirect(H)
		else:B=forms.InfoHoaxForm(instance=D,label_suffix='');messages.info(A,mMsgBox.get(_a))
	elif C==_G:D=get_object_or_404(J);D.delete();messages.info(A,mMsgBox.get(_G,D.name));return redirect(H)
	G='info hoaks';M=models.menu.objects.filter(nama=G,is_admin_menu=_B);N={_K:F.get_menus(),_Q:F.create_breadCrumb(G),_R:F.find_activeMenuList(G),_V:C,_U:B,_S:get_namaOPD(E),_T:M};return render(A,'account/info-hoax.html',N)
@login_required(login_url=_O)
def banner_all(request,mode='',pk='',photoID=''):
	T='/dashboard/banner-all';K=photoID;D=mode;A=request;cek_user(A);G=get_siteID(A)
	if G!=1:messages.info(A,_AP);return redirect(_A8)
	P=menus.ClsMenus(G,_B);B=_H;E=_H;K=[];H=''
	if D==_J or D==_G:
		if pk=='':return HttpResponse(_Y)
		Z=crypt_uuid4.ClsCryptUuid4();H=Z.dec_text(pk)
		if H=='':return HttpResponse(_Z)
		U=models.banner_all.objects.filter(id=H);a=models.banner_all.objects.filter(id=H)
		for C in a:K.append(C.photo.id)
	elif D==_M:I=formset_factory(forms.PhotoForm)
	if D==_M:
		if A.method==_I:
			B=forms.BannerAllForm(A.POST);E=I(A.POST)
			if B.is_valid():
				print('form valid');C=0
				for b in E:
					J=A.POST.get(_L+str(C)+_b)
					if J:
						L=J.replace(_t,'');M=models.photo.Jenis.BANNER_ALL;N=models.photo.objects.create(site_id=G,jenis=M,file_path=L);Q=B.cleaned_data.get('site');F=B.save(commit=_C);F.photo_id=N.id;F.save()
						for R in Q:F.site.add(R)
					C+=1
			return redirect(T)
		else:B=forms.BannerAllForm(label_suffix='');E=I();messages.info(A,mMsgBox.get(_W))
	elif D==_J:
		V=get_object_or_404(U);I=modelformset_factory(models.photo,form=forms.PhotoForm,extra=1-len(K))
		if A.method==_I:
			B=forms.BannerAllForm(A.POST,instance=V);E=I(A.POST)
			if B.is_valid():
				Q=B.cleaned_data.get('site');models.banner_all.site.through.objects.filter(banner_all_id=H).delete();F=B.save();C=0
				for b in E:
					J=A.POST.get(_L+str(C)+_b)
					if J:
						L=J.replace(_t,'');M=models.photo.Jenis.BANNER_ALL;W=A.POST.get(_L+str(C)+_c)
						if W:N,c=models.photo.objects.update_or_create(id=W,defaults={_u:G,_s:M,_o:L})
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
	S='Banner All';d=models.menu.objects.filter(nama=S,is_admin_menu=_B);e={_K:P.get_menus(),_Q:P.create_breadCrumb(S),_R:P.find_activeMenuList(S),_V:D,_U:B,_p:E,_S:get_namaOPD(G),_T:d};return render(A,'account/banner-all.html',e)
def social_media_ajax(request):
	C=get_siteID(request);A=models.social_media.objects.filter(site_id=C).values(_A,_s,_f,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def instansi_ajax(request):
	C=get_siteID(request);A=models.instansi.objects.filter(site_id=C).values(_A,_E,_A9,'telp',_A0,_AA,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def logo_ajax(request):
	C=get_siteID(request);A=models.logo.objects.filter(site_id=C).values(_A,'position',_v,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def banner_ajax(request):
	C=get_siteID(request);A=models.banner.objects.filter(site_id=C).values(_A,'position',_v,_f,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_ajax(request):
	C=get_siteID(request);A=models.menu.objects.filter(site__id=C,is_admin_menu=_C,is_master_menu=_C).values(_A,_E,'href','icon',_w,_D).order_by(_m,_x)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def menu_statis_ajax(request):A=get_siteID(request);B=models.menu.objects.filter(site__id=A,is_statis_menu=_B,is_admin_menu=_C).exclude(href='#').order_by(_m,_x);C=serializers.serialize('json',B,fields=(_A,_E));return HttpResponse(C,content_type='application/json')
def berita_ajax(request):
	C='photo__berita__id';D=get_siteID(request);E={'berita__id':OuterRef(C)};B=models.berita.objects.filter(site_id=D).values(_A,_F,_A3,'kategori__nama',_d,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A3]=Truncator(A[_A3]).chars(50)
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
	C='photo__pengumuman__id';D=get_siteID(request);E={'pengumuman__id':OuterRef(C)};B=models.pengumuman.objects.filter(site_id=D).values(_A,_F,_A4,_d,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A4]=Truncator(A[_A4]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def artikel_ajax(request):
	C='photo__artikel__id';D=get_siteID(request);E={'artikel__id':OuterRef(C)};B=models.artikel.objects.filter(site_id=D).values(_A,_F,_A5,_d,_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_A5]=Truncator(A[_A5]).words(30)
	F=list(B);return JsonResponse(F,safe=_C)
def dokumen_ajax(request):
	C='size';B=request;E=get_siteID(B);D=models.dokumen.objects.filter(site_id=E).values(_A,_E,_q,C,_o,_o,_D)
	for A in D:A[_D]=get_natural_datetime(A[_D]);A[C]=naturalsize(A[C]);A['extra_field']='%s://%s%s%s'%(B.scheme,B.get_host(),settings.MEDIA_URL,A[_o])
	F=list(D);return JsonResponse(F,safe=_C)
def agenda_ajax(request):
	C=get_siteID(request);B=models.agenda.objects.filter(site_id=C).values(_A,_E,_q,'lokasi',_AH,'jam','penyelenggara','dihadiri_oleh',_d,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_q]=Truncator(A[_q]).words(30)
	D=list(B);return JsonResponse(D,safe=_C)
def pejabat_ajax(request,pIsDefault):
	C=get_siteID(request);A=models.pejabat.objects.filter(site__id=C,is_default=pIsDefault).values(_A,_E,_AG,_v,_D).order_by(_c)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def link_terkait_ajax(request):
	C=get_siteID(request);A=models.link_terkait.objects.filter(site__id=C).values(_A,_E,_f,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def halaman_statis_ajax(request):
	C='photo__halaman_statis__id';D=get_siteID(request);E={'halaman_statis__id':OuterRef(C)};B=models.halaman_statis.objects.filter(site_id=D).values(_A,_F,_y,'menu__nama',_D).distinct().annotate(foto=get_topFoto(E)).annotate(foto_count=Count(C))
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_y]=Truncator(A[_y]).chars(50)
	F=list(B);return JsonResponse(F,safe=_C)
def galery_foto_ajax(request):
	C=get_siteID(request);B=models.galery_foto.objects.filter(site_id=C).values(_A,_F,_q,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5);A[_q]=Truncator(A[_q]).words(30)
	D=list(B);return JsonResponse(D,safe=_C)
def popup_ajax(request):
	C=get_siteID(request);A=models.popup.objects.filter(site_id=C).values(_A,_F,_v,_d,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	D=list(A);return JsonResponse(D,safe=_C)
def komentar_ajax(request):
	A='created_at';D=get_siteID(request);B=models.comment.objects.filter(site_id=D).values(_A,_l,_A0,'body','post__judul',A,'active')
	for C in B:C[A]=get_natural_datetime(C[A])
	E=list(B);return JsonResponse(E,safe=_C)
def galery_layanan_ajax(request):
	C=get_siteID(request);B=models.galery_layanan.objects.filter(site_id=C).values(_A,_F,_d,_v,_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def galery_video_ajax(request):
	C=get_siteID(request);B=models.galery_video.objects.filter(site_id=C).values(_A,_F,'embed',_D)
	for A in B:A[_D]=get_natural_datetime(A[_D]);A[_F]=Truncator(A[_F]).words(5)
	D=list(B);return JsonResponse(D,safe=_C)
def info_hoax_ajax(request):
	D=get_siteID(request);A=models.info_hoax.objects.all().values(_A,_l,_f,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def banner_all_ajax(request):
	D=get_siteID(request);A=models.banner_all.objects.all().values(_A,_l,_f,_v,_d,_D)
	for B in A:B[_D]=get_natural_datetime(B[_D])
	C=list(A);return JsonResponse(C,safe=_C)
def enc_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.enc_text(data))
def dec_text(request,data):A=crypt_uuid4.ClsCryptUuid4();return HttpResponse(A.dec_text(data))
def toggle_comment_activate(request,pID):A=models.comment.objects.get(id=pID);A.active^=_B;A.save();return HttpResponse('True')
def toggle_comment_activate_all(request):A=models.comment.objects.filter(site_id=get_siteID(request),active=_C).update(active=_B);return HttpResponse('True')
def top_kontributor_berita(request):
	F=models.berita.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for (C,E) in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);break
		elif not B and len(A)<6:
			print(_AQ)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_e))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_pengumuman(request):
	F=models.pengumuman.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for (C,E) in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E])
			if D==C:B=_B
		elif B and len(A)<6:print('found');A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);break
		elif not B and len(A)<6:
			print(_AQ)
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_e))+[0])
	return JsonResponse(A,safe=_C)
def top_kontributor_artikel(request):
	F=models.artikel.objects.exclude(admin_id=1).values_list(_AI).annotate(jumlah=Count(_A)).order_by(_AJ);A=[];B=_C;D=request.user.id
	for (C,E) in F:
		if len(A)<5:
			A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E])
			if D==C:B=_B
		elif B and len(A)<6:A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);break
		elif not B and len(A)<6:
			if D==C:A.append(list(models.User.objects.filter(id=C).values_list(_A,_e))+[E]);B=_B;break
	if not B:A.append(list(models.User.objects.filter(id=D).values_list(_A,_e))+[0]);print('res = ');print(A)
	return JsonResponse(A,safe=_C)
def site_activity(request):
	D=[];G=list(models.Site.objects.exclude(id=1).order_by(_N).values(_A,_N))
	for A in G:
		B=[];H=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for I in H:B.append(I[_A])
		J=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=B);C=len(B);E=J.filter(is_edited=_B).count()
		if C==0:F=0
		else:F=E/C*100
		K={_A:A[_A],_N:A[_N],_A7:C,_n:E,_z:F};D.append(K)
	return JsonResponse(D,safe=_C)
def site_activity_pie_chart(request):
	C=[];P=list(models.Site.objects.exclude(id=1).order_by(_N).values(_A,_N));Q=0
	for A in P:
		D=[];R=list(models.menu.objects.filter(site__id=A[_A],is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).values(_A))
		for S in R:D.append(S[_A])
		T=models.halaman_statis.objects.filter(site__id=A[_A],menu__id__in=D);E=len(D);H=T.filter(is_edited=_B).count()
		if E==0:F=0
		else:F=H/E*100
		Q+=F;U={_A:A[_A],_N:A[_N],_A7:E,_n:H,_z:F};C.append(U)
	C=sorted(C,key=lambda x:x[_z],reverse=_B);B=[];I=10;J=0;K=0;L=0;M=0;G=_C;N=get_siteID(request);O=0
	for A in C:
		J+=1
		if J<I:
			B.append(A)
			if A[_A]==N:G=_B;print(_AK)
		elif len(B)<=I:
			if G:B.append(A);G=_C;print(_AL)
			elif A[_A]==N:B.append(A)
			else:K+=A[_n];L+=A[_A7];M+=A[_z];O+=1
		else:K+=A[_n];L+=A[_A7];M+=A[_z];O+=1
	return JsonResponse(B,safe=_C)
def site_activity_detail(request,siteID):
	B=siteID;C=[];H=[];F=list(models.menu.objects.filter(site__id=B,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AE,_x).values(_A,_E,_w))
	for A in F:
		D=models.halaman_statis.objects.filter(site__id=B,menu__id=A[_A],is_edited=_B)[:1]
		if D:
			for G in D:E={_A:A[_A],_m:A[_w],_K:A[_E],_F:G.judul,_n:1}
		else:E={_A:A[_A],_m:A[_w],_K:A[_E],_F:'',_n:0}
		C.append(E)
	return JsonResponse(C,safe=_C)
def site_activity_detail_pie_chart(request,siteID):
	F=siteID;B=[];L=[];I=list(models.menu.objects.filter(site__id=F,is_admin_menu=_C,is_statis_menu=_B,is_visibled=_B).order_by(_AE,_x).values(_A,_E,_w))
	for A in I:
		G=models.halaman_statis.objects.filter(site__id=F,menu__id=A[_A],is_edited=_B)[:1]
		if G:
			for J in G:H={_A:A[_A],_m:A[_w],_K:A[_E],_F:J.judul,_n:1}
		else:H={_A:A[_A],_m:A[_w],_K:A[_E],_F:'',_n:0}
		B.append(H)
	print('begin create pie chart data');E=len(B);print(E);C=len(list(filter(lambda x:x[_n]==0,B)));print(C);D=len(list(filter(lambda x:x[_n]==1,B)));print(D);C=C/E*100;D=D/E*100;K=[{_l:'Menu Terisi','y':D,'sliced':_B,'selected':_B},{_l:'Menu Kosong','y':C}];return JsonResponse(K,safe=_C)
def site_productivity(request):
	B=[];F=list(models.Site.objects.exclude(id=1).order_by(_N).values(_A,_N))
	for A in F:I=[];C=models.berita.objects.filter(site_id=A[_A]).count();D=models.artikel.objects.filter(site_id=A[_A]).count();E=models.pengumuman.objects.filter(site_id=A[_A]).count();G=C+D+E;H={_A:A[_A],_N:A[_N],_i:C,_j:E,_k:D,_h:G};B.append(H)
	B=sorted(B,key=lambda x:x[_h],reverse=_B);return JsonResponse(B,safe=_C)
def site_kontribusi_kuantitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[]
	if J==1:L=list(models.Site.objects.exclude(id=1).order_by(_N).values(_A,_N))
	else:
		S=list(models.instansi.objects.filter(kategori_id=J).values(_u))
		for A in S:K.append(A[_u])
		L=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_N).values(_A,_N))
	for A in L:W=[];M=models.berita.objects.filter(site_id=A[_A]).count();N=models.artikel.objects.filter(site_id=A[_A]).count();O=models.pengumuman.objects.filter(site_id=A[_A]).count();T=M+N+O;U={_A:A[_A],_N:A[_N],_i:M,_j:O,_k:N,_h:T};C.append(U)
	C=sorted(C,key=lambda x:x[_h],reverse=_B);B=[];P=10;Q=0;D=0;E=0;F=0;G=0;H=_C;R=get_siteID(request);I=0
	for A in C:
		Q+=1
		if Q<P:
			B.append(A)
			if A[_A]==R:H=_B;print(_AK)
		elif len(B)<=P:
			if H:B.append(A);H=_C;print(_AL)
			elif A[_A]==R:B.append(A)
			else:D+=A[_i];E+=A[_j];F+=A[_k];G+=A[_h];I+=1
		else:D+=A[_i];E+=A[_j];F+=A[_k];G+=A[_h];I+=1
	V={_A:0,_N:_AR+str(I)+_AS,_i:D,_j:E,_k:F,_h:G};B.append(V);return JsonResponse(B,safe=_C)
def site_kontribusi_kualitas_pie_chart(request,kategori_id):
	J=kategori_id;C=[];K=[];L=500;T=300
	if J==1:M=list(models.Site.objects.exclude(id=1).order_by(_N).values(_A,_N))
	else:
		U=list(models.instansi.objects.filter(kategori_id=J).values(_u))
		for A in U:K.append(A[_u])
		M=list(models.Site.objects.filter(id__in=K).exclude(id=1).order_by(_N).values(_A,_N))
	for A in M:Y=[];N=models.berita.objects.filter(site_id=A[_A],word_count__gte=L).count();O=models.artikel.objects.filter(site_id=A[_A],word_count__gte=L).count();P=models.pengumuman.objects.filter(site_id=A[_A],word_count__gte=T).count();V=N+O+P;W={_A:A[_A],_N:A[_N],_i:N,_j:P,_k:O,_h:V};C.append(W)
	C=sorted(C,key=lambda x:x[_h],reverse=_B);B=[];Q=10;R=0;D=0;E=0;F=0;G=0;H=_C;S=get_siteID(request);I=0
	for A in C:
		R+=1
		if R<Q:
			B.append(A)
			if A[_A]==S:H=_B;print(_AK)
		elif len(B)<=Q:
			if H:B.append(A);H=_C;print(_AL)
			elif A[_A]==S:B.append(A)
			else:D+=A[_i];E+=A[_j];F+=A[_k];G+=A[_h];I+=1
		else:D+=A[_i];E+=A[_j];F+=A[_k];G+=A[_h];I+=1
	X={_A:0,_N:_AR+str(I)+_AS,_i:D,_j:E,_k:F,_h:G};B.append(X);return JsonResponse(B,safe=_C)
def site_ajax(request):
	A=request.GET.get('search')
	if A:B=models.Site.objects.filter(domain__icontains=A).exclude(id=1).values(_A,text=F(_N))
	else:B=models.Site.objects.exclude(id=1).values(_A,text=F(_N))
	return JsonResponse({'results':list(B),_AT:{'more':_B}},safe=_C)
def instansi_kategori_ajax(request):
	A=request.GET.get('search')
	if A:B=models.instansi_kategori.objects.filter(nama__icontains=A).values(_A,text=F(_E))
	else:B=models.instansi_kategori.objects.values(_A,text=F(_E))
	return JsonResponse({'results':list(B),_AT:{'more':_B}},safe=_C)