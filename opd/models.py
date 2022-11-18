_D='{} - {}'
_C='/%s/%s'
_B=False
_A=True
import os,random,re,string
from bs4 import BeautifulSoup as bs
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django_opd.commonf import get_natural_datetime
from embed_video.fields import EmbedVideoField
from PIL import Image
def custom_slugify(text_to_slugify,site_id,field_length):
	E=field_length;D=site_id;C=text_to_slugify;print('load custom slugify')
	if D:F=str(D);A=E-len(F)-2;B=slugify(C);return B[:A]+'--'+F
	else:A=E;B=slugify(C);return B[:A]
def word_count(text):A=bs(text,'html.parser');B=A.get_text();return sum([A.strip(string.punctuation).isalpha()for A in B.split()])
class Status(models.TextChoices):DRAFT='draft';PUBLISHED='published'
class photo(models.Model):
	class Jenis(models.TextChoices):LOGO_TOP='logo-top';LOGO_BOTTOM='logo-bottom';BANNER_TOP='banner-top';BANNER_MIDDLE1='banner-middle1';BANNER_MIDDLE2='banner-middle2';BANNER_BOTTOM='banner-bottom';HIGHLIGHT1='highlight1';HIGHLIGHT2='highlight2';HIGHLIGHT3='highlight3';BUPATI='bupati';WABUP='wabup';SEKDA='sekda';PEJABAT_OPD='pejabat-opd';POPUP='popup';BANNER_ALL='banner-all'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);file_path=models.ImageField();jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.HIGHLIGHT1,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.file_path.url
class kategori(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);count=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=custom_slugify(A.nama,None,50);super(kategori,A).save(*(B),**C)
class tags(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=custom_slugify(A.nama,None,50);super(tags,A).save(*(B),**C)
class berita(models.Model):
	kategori=models.ForeignKey(kategori,on_delete=models.PROTECT);site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_berita=RichTextUploadingField(blank=_A,null=_A);view_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);tags=models.ManyToManyField(tags,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _C%('berita',A.judul_seo)
	def save(A,*B,**C):A.judul_seo=custom_slugify(A.judul,A.site.id,255);A.word_count=word_count(A.isi_berita);super(berita,A).save(*(B),**C)
	@property
	def created_at_(self):return get_natural_datetime(self.created_at)
class comment(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);post=models.ForeignKey(berita,on_delete=models.PROTECT);name=models.CharField(max_length=80);email=models.EmailField();body=models.TextField();created_at=models.DateTimeField(auto_now_add=_A);active=models.BooleanField(default=_B)
	class Meta:ordering=['created_at']
	def __str__(A):return 'Comment {} by {}'.format(A.body,A.name)
class pengumuman(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_pengumuman=RichTextUploadingField(blank=_A,null=_A);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _C%('pengumuman',A.judul_seo)
	def save(A,*B,**C):A.judul_seo=custom_slugify(A.judul,A.site.id,255);A.word_count=word_count(A.isi_pengumuman);super(pengumuman,A).save(*(B),**C)
class artikel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_artikel=RichTextUploadingField(blank=_A,null=_A);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _C%('artikel',A.judul_seo)
	def save(A,*B,**C):A.judul_seo=custom_slugify(A.judul,A.site.id,255);A.word_count=word_count(A.isi_artikel);super(artikel,A).save(*(B),**C)
class dokumen(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);file_path=models.FileField();nama=models.CharField(max_length=150);deskripsi=RichTextUploadingField(blank=_A,null=_A);size=models.BigIntegerField(null=_A,blank=_A,default=0);hits=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED)
	def __str__(A):return A.nama
class link_terkait(models.Model):
	site=models.ManyToManyField(Site,blank=_A);link=models.URLField(max_length=200);nama=models.CharField(max_length=150);icon_awesome=models.TextField(null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class galery_foto(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);deskripsi=RichTextUploadingField(blank=_A,null=_A);view_count=models.IntegerField(default=0);link=models.URLField(max_length=200,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(A,*B,**C):A.judul_seo=custom_slugify(A.judul,A.site.id,255);super(galery_foto,A).save(*(B),**C)
class galery_layanan(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);link=models.URLField(max_length=200,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
class galery_video(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);view_count=models.IntegerField(default=0);embed=RichTextUploadingField(blank=_A,null=_A,config_name='embed_video');embed_video=EmbedVideoField(blank=_A,null=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(C,*G,**H):
		F='src';E=0;A='';I=C.embed.split(' ');B=_B
		for J in I:
			if B:break
			K=J.split('=');B=_B
			for D in K:
				if not B and D.lower()==F:B=_A
				if B and D.lower()!=F:
					if E==0:A+=D;E+=1
					else:A+='='+D
					print(A)
		if A.find('watch')<=0:A=A.replace('"','');A=A.replace('&quot;','');C.embed_video=A
		else:C.embed_video=None
		super(galery_video,C).save(*(G),**H)
class instansi_kategori(models.Model):
	nama=models.CharField(max_length=50);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return '{}'.format(A.nama)
class instansi(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ManyToManyField(User,blank=_A);nama=models.CharField(max_length=255);alamat=models.CharField(max_length=255,null=_A,blank=_A);telp=models.CharField(max_length=100,null=_A,blank=_A);email=models.EmailField(max_length=150,null=_A,blank=_A);kode_post=models.CharField(max_length=50,null=_A,blank=_A);kategori=models.ForeignKey(instansi_kategori,null=_A,blank=_A,on_delete=models.PROTECT);parent=models.ForeignKey('self',null=_A,blank=_A,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _D.format(A.site.name,A.nama)
class social_media(models.Model):
	class Jenis(models.TextChoices):FACEBOOK='facebook';TWITTER='twitter';PINTEREST='pinterest';YOUTUBE='youtube';INSTAGRAM='instagram'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.FACEBOOK);link=models.URLField(max_length=200);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _D.format(A.site.name,A.jenis)
class logo(models.Model):
	class Position(models.TextChoices):TOP='TOP';BOTTOM='BOTTOM'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);photo=models.ForeignKey(photo,on_delete=models.CASCADE,blank=_A);position=models.CharField(max_length=20,choices=Position.choices,default=Position.TOP);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _D.format(A.site.name,A.position)
class banner(models.Model):
	class Position(models.TextChoices):TOP='top';MIDDLE1='middle1';MIDDLE2='middle2';BOTTOM='bottom'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);photo=models.ForeignKey(photo,on_delete=models.CASCADE);link=models.URLField(max_length=200,null=_A,blank=_A);position=models.CharField(max_length=20,choices=Position.choices,default=Position.TOP);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
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
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);jabatan=models.CharField(max_length=50);jabatan_index=models.CharField(max_length=50,choices=Position.choices,default=Position.PEJABAT_OPD);photo=models.ForeignKey(photo,on_delete=models.CASCADE,blank=_A);admin=models.ForeignKey(User,on_delete=models.PROTECT);is_default=models.BooleanField(default=_B);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class no_penting(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);nama=models.CharField(max_length=30);jabatan=models.CharField(max_length=50,null=_A,blank=_A);nomor=models.CharField(max_length=20);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class halaman_statis(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);judul=models.CharField(max_length=500);isi_halaman=RichTextUploadingField(blank=_A,null=_A);photo=models.ManyToManyField(photo,blank=_A);view_count=models.IntegerField(default=0);menu=models.ForeignKey(menu,on_delete=models.PROTECT);admin=models.ForeignKey(User,on_delete=models.PROTECT,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A);is_edited=models.BooleanField(default=_B)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _C%('halaman statis',A.judul)
class page_widget(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);lokasi=models.CharField(max_length=255);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=RichTextUploadingField(blank=_A,null=_A);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=custom_slugify(A.nama,A.site.id,50);super(page_widget,A).save(*(B),**C)
class agenda(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);nama=models.CharField(max_length=500);nama_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);deskripsi=RichTextUploadingField(blank=_A,null=_A);lokasi=models.CharField(max_length=30,null=_A,blank=_A);tanggal=models.DateField();jam=models.TimeField();penyelenggara=models.CharField(max_length=100,null=_A,blank=_A);dihadiri_oleh=models.CharField(max_length=100,null=_A,blank=_A);view_count=models.IntegerField(default=0);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=custom_slugify(A.nama,A.site.id,255);super(agenda,A).save(*(B),**C)
class page_rss(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=RichTextUploadingField(blank=_A,null=_A);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=custom_slugify(A.nama,A.site.id,50);super(page_rss,A).save(*(B),**C)
class popup(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);link=models.URLField(max_length=200,null=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.photo
	def save(A,*B,**C):A.judul_seo=custom_slugify(A.judul,A.site.id,255);super(popup,A).save(*(B),**C)
class info_hoax(models.Model):
	name=models.CharField(max_length=100);slug=models.SlugField(max_length=100,default='',unique=_A,blank=_A);link=models.URLField(max_length=200);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
	def save(A,*B,**C):A.slug=custom_slugify(A.name,'',100);super(info_hoax,A).save(*(B),**C)
class banner_all(models.Model):
	site=models.ManyToManyField(Site,blank=_A);name=models.CharField(max_length=50);link=models.URLField(max_length=200,null=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
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