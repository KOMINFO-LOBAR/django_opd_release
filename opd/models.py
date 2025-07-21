_J='html.parser'
_I='nama_seo'
_H='{} - {}'
_G='/%s/%s'
_F='judul_seo'
_E=None
_D='src'
_C='extends'
_B=False
_A=True
import os,string,uuid,pytz,datetime,shutil
from django.utils import timezone
from PIL import Image
from bs4 import BeautifulSoup as bs
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field
from embed_video.fields import EmbedVideoField
from uuslug import uuslug
from dateutil import parser
from django_opd.commonf import get_natural_datetime
from django.conf import settings
from bs4 import BeautifulSoup
from easy_thumbnails.files import get_thumbnailer
from pathlib import Path
from account.compress_image import compress_img
from account.resize_image import resize_width_to
from hitcount.models import Hit
from outbox_hitcount.hit_summary import do_summary
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin
from hitcount.settings import MODEL_HITCOUNT
def word_count(text):A=bs(text,_J);B=A.get_text();return sum([A.strip(string.punctuation).isalpha()for A in B.split()])
class Status(models.TextChoices):DRAFT='draft';PUBLISHED='published'
class photo(models.Model):
	class Jenis(models.TextChoices):LOGO_TOP='logo-top';LOGO_BOTTOM='logo-bottom';BANNER_TOP='banner-top';BANNER_MIDDLE1='banner-middle1';BANNER_MIDDLE2='banner-middle2';BANNER_BOTTOM='banner-bottom';HIGHLIGHT1='highlight1';HIGHLIGHT2='highlight2';HIGHLIGHT3='highlight3';HIGHLIGHT_EDITOR='highlight-editor';BUPATI='bupati';WABUP='wabup';SEKDA='sekda';PEJABAT_OPD='pejabat-opd';POPUP='popup';BANNER_ALL='banner-all'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);file_path=models.ImageField(max_length=255);jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.HIGHLIGHT1,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.file_path.url
class kategori(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);count=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=uuslug(A.nama,instance=A,max_length=50);super().save(*(B),**C)
class tags(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=uuslug(A.nama,instance=A,max_length=50);super().save(*(B),**C)
class berita(models.Model,HitCountMixin):
	kategori=models.ForeignKey(kategori,on_delete=models.PROTECT);site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_berita=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);hit_count_generic=GenericRelation(MODEL_HITCOUNT,object_id_field='object_pk',related_query_name='hit_count_generic_relation');tags=models.ManyToManyField(tags,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):B=A.site.domain;return'https://%s/%s/%s'%(B,'berita',A.slug)
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.judul,instance=A,slug_field='slug',max_length=255)
		A.word_count=word_count(A.isi_berita);super().save(*(B),**C)
	@property
	def created_at_(self):return get_natural_datetime(self.created_at)
class comment(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);post=models.ForeignKey(berita,on_delete=models.PROTECT);name=models.CharField(max_length=80);email=models.EmailField();body=models.TextField();created_at=models.DateTimeField(auto_now_add=_A);active=models.BooleanField(default=_B)
	class Meta:ordering=['created_at']
	def __str__(A):return 'Comment {} by {}'.format(A.body,A.name)
class pengumuman(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_pengumuman=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _G%('pengumuman',A.judul_seo)
	def save(A,*B,**C):
		if not A.judul_seo:A.judul_seo=uuslug(A.judul,instance=A,slug_field=_F,max_length=255)
		A.word_count=word_count(A.isi_pengumuman);super().save(*(B),**C)
class artikel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_artikel=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _G%('artikel',A.judul_seo)
	def save(A,*B,**C):
		if not A.judul_seo:A.judul_seo=uuslug(A.judul,instance=A,slug_field=_F,max_length=250)
		A.word_count=word_count(A.isi_artikel);super().save(*(B),**C)
class dokumen_kategori(models.Model):
	nama=models.CharField(max_length=50);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return '{}'.format(A.nama)
class dokumen(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);file_path=models.FileField();nama=models.CharField(max_length=150);deskripsi=CKEditor5Field(blank=_A,null=_A,config_name=_C);size=models.BigIntegerField(null=_A,blank=_A,default=0);hits=models.IntegerField(default=0);kategori=models.ForeignKey(dokumen_kategori,null=_A,blank=_A,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED)
	def __str__(A):return A.nama
class link_terkait(models.Model):
	site=models.ManyToManyField(Site,blank=_A);link=models.URLField(max_length=200);nama=models.CharField(max_length=150);icon_awesome=models.TextField(null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class galery_foto(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);view_count=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(A,*B,**C):
		if not A.judul_seo:A.judul_seo=uuslug(A.judul,instance=A,slug_field=_F,max_length=255)
		super().save(*(B),**C)
class galery_layanan(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);link=models.URLField(max_length=200,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
def save_embed_video(embed):
	D=0;A='';E=embed.split(' ');B=_B
	for F in E:
		if B:break
		G=F.split('=');B=_B
		for C in G:
			if not B and C.lower()==_D:B=_A
			if B and C.lower()!=_D:
				if D==0:A+=C;D+=1
				else:A+='='+C
	if A.find('watch')<=0:A=A.replace('"','');A=A.replace('&quot;','');return A
	else:return _E
class galery_video(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);view_count=models.IntegerField(default=0);embed=CKEditor5Field(blank=_A,null=_A,config_name=_C);embed_video=EmbedVideoField(blank=_A,null=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(A,*B,**C):A.embed_video=save_embed_video(A.embed);super().save(*(B),**C)
class instansi_kategori(models.Model):
	nama=models.CharField(max_length=50);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return '{}'.format(A.nama)
class instansi(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ManyToManyField(User,blank=_A);nama=models.CharField(max_length=255);alamat=models.CharField(max_length=255,null=_A,blank=_A);telp=models.CharField(max_length=100,null=_A,blank=_A);email=models.EmailField(max_length=150,null=_A,blank=_A);kode_post=models.CharField(max_length=50,null=_A,blank=_A);kategori=models.ForeignKey(instansi_kategori,null=_A,blank=_A,on_delete=models.PROTECT);parent=models.ForeignKey('self',null=_A,blank=_A,on_delete=models.PROTECT);histats=models.TextField(blank=_A,null=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _H.format(A.site.name,A.nama)
class social_media(models.Model):
	class Jenis(models.TextChoices):FACEBOOK='facebook';TWITTER='twitter';PINTEREST='pinterest';YOUTUBE='youtube';INSTAGRAM='instagram'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.FACEBOOK);link=models.URLField(max_length=200);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _H.format(A.site.name,A.jenis)
class logo(models.Model):
	class Position(models.TextChoices):TOP='TOP';BOTTOM='BOTTOM'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);photo=models.ForeignKey(photo,on_delete=models.CASCADE,blank=_A);position=models.CharField(max_length=20,choices=Position.choices,default=Position.TOP);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _H.format(A.site.name,A.position)
class banner(models.Model):
	class Position(models.TextChoices):TOP='top';MIDDLE1='middle1';MIDDLE2='middle2';BOTTOM='bottom'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);photo=models.ForeignKey(photo,on_delete=models.CASCADE);link=models.URLField(max_length=200,null=_A,blank=_A);position=models.CharField(max_length=20,choices=Position.choices);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.position
class menu(models.Model):
	site=models.ManyToManyField(Site,blank=_A);parent=models.ForeignKey('self',null=_A,blank=_A,on_delete=models.PROTECT);nama=models.CharField(max_length=100);href=models.CharField(max_length=255,null=_A,blank=_A,verbose_name='Link');icon=models.CharField(max_length=50,null=_A,blank=_A);order_menu=models.IntegerField(default=0);is_admin_menu=models.BooleanField(default=_B);is_visibled=models.BooleanField(default=_A);is_master_menu=models.BooleanField(default=_B);is_statis_menu=models.BooleanField(default=_B);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):
		if A.is_admin_menu:B='[ Admin ]'
		else:B='[ Front End ]'
		if A.parent:C=A.parent.nama
		else:C=''
		return '{} {} > {}'.format(B,C,A.nama)
class statistik(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);ip=models.CharField(max_length=20);hits=models.IntegerField(default=0);tanggal=models.DateTimeField(auto_now_add=_A)
	def __str__(A):return A.ip
class pejabat(models.Model):
	class Position(models.TextChoices):BUPATI='1';WABUP='2';SEKDA='3';PEJABAT_OPD='4'
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);jabatan=models.CharField(max_length=50);jabatan_index=models.CharField(max_length=50,choices=Position.choices,default=Position.PEJABAT_OPD);photo=models.ForeignKey(photo,on_delete=models.CASCADE,blank=_A);admin=models.ForeignKey(User,on_delete=models.PROTECT,blank=_A);is_default=models.BooleanField(default=_B);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class no_penting(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);nama=models.CharField(max_length=30);jabatan=models.CharField(max_length=50,null=_A,blank=_A);nomor=models.CharField(max_length=20);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class halaman_statis(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);judul=models.CharField(max_length=500);isi_halaman=CKEditor5Field(blank=_A,null=_A,config_name=_C);photo=models.ManyToManyField(photo,blank=_A);view_count=models.IntegerField(default=0);menu=models.ForeignKey(menu,on_delete=models.PROTECT);admin=models.ForeignKey(User,on_delete=models.PROTECT,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A);is_edited=models.BooleanField(default=_B)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _G%('halaman statis',A.judul)
class page_widget(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);lokasi=models.CharField(max_length=255);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=CKEditor5Field(blank=_A,null=_A,config_name=_C);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):
		if not A.nama_seo:A.nama_seo=uuslug(A.nama,instance=A,slug_field=_I,max_length=50)
		super().save(*(B),**C)
class agenda(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);nama=models.CharField(max_length=500);nama_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);deskripsi=CKEditor5Field(blank=_A,null=_A,config_name=_C);lokasi=models.CharField(max_length=30,null=_A,blank=_A);tanggal=models.DateField();jam=models.TimeField();penyelenggara=models.CharField(max_length=100,null=_A,blank=_A);dihadiri_oleh=models.CharField(max_length=100,null=_A,blank=_A);view_count=models.IntegerField(default=0);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):
		if not A.nama_seo:A.nama_seo=uuslug(A.nama,instance=A,slug_field=_I,max_length=255)
		super().save(*(B),**C)
class page_rss(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=CKEditor5Field(blank=_A,null=_A,config_name=_C);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):
		if not A.nama_seo:A.nama_seo=uuslug(A.nama,instance=A,slug_field=_I,max_length=50)
		super().save(*(B),**C)
class popup(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);link=models.URLField(max_length=200,null=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.photo
	def save(A,*B,**C):
		if not A.judul_seo:A.judul_seo=uuslug(A.judul,instance=A,slug_field=_F,max_length=255)
		super().save(*(B),**C)
class info_hoax(models.Model):
	name=models.CharField(max_length=255);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A);link=models.URLField(max_length=255);publish_date=models.CharField(max_length=50,null=_A,blank=_A);publish_date_convert=models.DateTimeField(null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
	def save(A,*B,**C):
		A.slug=uuslug(A.name,instance=A,max_length=255)
		if A.publish_date_convert is _E:A.publish_date_convert=parser.parse(A.publish_date)
		super().save(*(B),**C)
class info_widget(models.Model):
	title=models.CharField(max_length=255);categori=models.CharField(max_length=100);publish_date=models.CharField(max_length=50);author=models.CharField(max_length=50);link=models.URLField(max_length=255);publish_date_convert=models.DateTimeField(null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.title
	def save(B,*C,**D):
		if B.publish_date_convert is _E:E=getattr(settings,'TIME_ZONE','UTC');F=pytz.timezone(E);A=parser.parse(B.publish_date);B.publish_date_convert=datetime.datetime(A.year,A.month,A.day,A.hour,A.minute,A.second,tzinfo=F)
		super().save(*(C),**D)
class banner_all(models.Model):
	site=models.ManyToManyField(Site,blank=_A);name=models.CharField(max_length=50);link=models.URLField(max_length=200,null=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
class Template(models.Model):
	uuid=models.UUIDField(unique=_A,default=uuid.uuid4,editable=_B);site=models.ManyToManyField(Site,related_name='templates_site',blank=_A);name=models.CharField('name',max_length=50);rel_path=models.CharField('relative path',max_length=255);is_frontend=models.BooleanField(default=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A,editable=_B);updated_at=models.DateTimeField(auto_now=_A,editable=_B)
	def get_sites(A):return ', '.join([A.domain for A in A.site.all()])
	def __str__(A):return A.name
class Weather(models.Model):
	kabkota=models.CharField('Kabupaten Kota',max_length=50);kec=models.CharField('Kecamatan',max_length=30);hari=models.CharField('Hari',max_length=20);tgl=models.DateTimeField();t=models.CharField('Temperatur',max_length=10);hu=models.CharField('Kelembapan',max_length=10);ws=models.CharField('Kecepatan Angin',max_length=10);wd=models.CharField('Arah Angin',max_length=10);weather_info=models.CharField('Info Cuaca',max_length=100);img=models.CharField('Icon',max_length=255)
	def __str__(A):return A.kabkota
def create_unique_filename(file_ext):A=datetime.datetime.now();return A.strftime('%Y%m%d-%H%M%S-%f')+'.'+file_ext
def get_site(domain):
	A=Site.objects.filter(domain=domain)
	if A:A=A.get();B=A.name.replace(' ','-');B=B.lower();C=A.id;return C,B
	return _E,_E
def clear_empty_array(split_path):
	B=split_path;A=0
	while A<len(B):
		if not B[A]:B.pop(A)
		else:A=A+1
def move_image(isi_berita,obj_photo,site_id,site_name):
	P='thumbnail/';K=isi_berita;F=site_name;B='/'
	if K:
		G=getattr(settings,'BASE_DIR','');L=BeautifulSoup(K,_J);M=1024;N=_B
		for H in L.findAll('img'):
			if _D in H:
				I=H[_D];A=I.split(B)
				if not('https:'in A or'http:'in A):
					clear_empty_array(A)
					if'thumbnail'in A and F in A:continue
					C=A[0];A.pop(0)
					if len(A)<=0:continue
					Q=A[len(A)-1];D=Q.split('.');D=D[len(D)-1];R=create_unique_filename(D);I=B.join(A);J=P+F+B+R;S=P+F;os.makedirs(os.path.join(G,C,S),exist_ok=_A);O=os.path.join(G,C,I);E=os.path.join(G,C,J)
					if os.path.isfile(O):
						shutil.move(O,E);compress_img(E,new_size_ratio=1,quality=80,replace=_A);T=Image.open(E);U,W=T.size[:2]
						if U>M:resize_width_to(E,M)
						V=photo.objects.create(site_id=site_id,jenis=photo.Jenis.HIGHLIGHT_EDITOR,file_path=J);obj_photo.append(V);H[_D]=B+C+B+J;N=_A
		return N,L
@receiver(models.signals.post_save,sender=berita)
@receiver(models.signals.post_save,sender=artikel)
@receiver(models.signals.post_save,sender=pengumuman)
@receiver(models.signals.post_save,sender=halaman_statis)
@receiver(models.signals.post_save,sender=dokumen)
def auto_relocate_image(sender,instance,**I):
	B=sender;A=instance;C,F=get_site(A.site)
	if C:
		D=[];E=_B
		if B==berita:
			if A.isi_berita:E,G=move_image(A.isi_berita,D,C,F)
		elif B==artikel:
			if A.isi_artikel:E,G=move_image(A.isi_artikel,D,C,F)
		elif B==pengumuman:
			if A.isi_pengumuman:E,G=move_image(A.isi_pengumuman,D,C,F)
		elif B==halaman_statis:
			if A.isi_halaman:E,G=move_image(A.isi_halaman,D,C,F)
		elif B==dokumen:
			if A.deskripsi:E,G=move_image(A.deskripsi,D,C,F)
		if E:
			B.objects.filter(id=A.id).update(isi_berita=str(G))
			for H in D:B.objects.get(id=A.id).photo.add(H)
@receiver(models.signals.post_delete,sender=dokumen)
@receiver(models.signals.post_delete,sender=photo)
def auto_delete_file_on_delete(sender,instance,**B):
	A=instance
	try:
		if A.file_path:
			if os.path.isfile(A.file_path.path):os.remove(A.file_path.path)
	finally:return _A
@receiver(models.signals.pre_save,sender=dokumen)
@receiver(models.signals.pre_save,sender=photo)
def auto_delete_file_on_change(sender,instance,**E):
	C=sender;B=instance
	if not B.pk:return _B
	try:A=C.objects.get(pk=B.pk).file_path
	except C.DoesNotExist:return _B
	try:
		D=B.file_path
		if not A==D:
			if A:
				if os.path.isfile(A.path):os.remove(A.path)
	finally:return _A