_G='nama_seo'
_F='{} - {}'
_E='/%s/%s'
_D='judul_seo'
_C='extends'
_B=False
_A=True
import os,string
from bs4 import BeautifulSoup as bs
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field
from embed_video.fields import EmbedVideoField
from uuslug import uuslug
from django_opd.commonf import get_natural_datetime
def word_count(text):A=bs(text,'html.parser');B=A.get_text();return sum([A.strip(string.punctuation).isalpha()for A in B.split()])
class Status(models.TextChoices):DRAFT='draft';PUBLISHED='published'
class photo(models.Model):
	class Jenis(models.TextChoices):LOGO_TOP='logo-top';LOGO_BOTTOM='logo-bottom';BANNER_TOP='banner-top';BANNER_MIDDLE1='banner-middle1';BANNER_MIDDLE2='banner-middle2';BANNER_BOTTOM='banner-bottom';HIGHLIGHT1='highlight1';HIGHLIGHT2='highlight2';HIGHLIGHT3='highlight3';BUPATI='bupati';WABUP='wabup';SEKDA='sekda';PEJABAT_OPD='pejabat-opd';POPUP='popup';BANNER_ALL='banner-all'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);file_path=models.ImageField();jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.HIGHLIGHT1,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.file_path.url
class kategori(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);count=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=uuslug(A.nama,instance=A,max_length=50);super().save(*B,**C)
class tags(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);slug=models.SlugField(max_length=50,default='',unique=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.slug=uuslug(A.nama,instance=A,max_length=50);super().save(*B,**C)
class berita(models.Model):
	kategori=models.ForeignKey(kategori,on_delete=models.PROTECT);site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_berita=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);tags=models.ManyToManyField(tags,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return f"/berita/{A.judul_seo}"
	def save(A,*B,**C):A.judul_seo=uuslug(A.judul,instance=A,slug_field=_D,max_length=255);A.word_count=word_count(A.isi_berita);super().save(*B,**C)
	@property
	def created_at_(self):return get_natural_datetime(self.created_at)
class comment(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);post=models.ForeignKey(berita,on_delete=models.PROTECT);name=models.CharField(max_length=80);email=models.EmailField();body=models.TextField();created_at=models.DateTimeField(auto_now_add=_A);active=models.BooleanField(default=_B)
	class Meta:ordering=['created_at']
	def __str__(A):return'Comment {} by {}'.format(A.body,A.name)
class pengumuman(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_pengumuman=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _E%('pengumuman',A.judul_seo)
	def save(A,*B,**C):A.judul_seo=uuslug(A.judul,instance=A,slug_field=_D,max_length=255);A.word_count=word_count(A.isi_pengumuman);super().save(*B,**C)
class artikel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=models.ManyToManyField(photo,blank=_A);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);isi_artikel=CKEditor5Field(blank=_A,null=_A,config_name=_C);view_count=models.IntegerField(default=0);share_count=models.IntegerField(default=0);word_count=models.IntegerField(default=0,blank=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def get_absolute_url(A):return _E%('artikel',A.judul_seo)
	def save(A,*B,**C):A.judul_seo=uuslug(A.judul,instance=A,slug_field=_D,max_length=255);A.word_count=word_count(A.isi_artikel);super().save(*B,**C)
class dokumen(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);file_path=models.FileField();nama=models.CharField(max_length=150);deskripsi=CKEditor5Field(blank=_A,null=_A,config_name=_C);size=models.BigIntegerField(null=_A,blank=_A,default=0);hits=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED)
	def __str__(A):return A.nama
class link_terkait(models.Model):
	site=models.ManyToManyField(Site,blank=_A);link=models.URLField(max_length=200);nama=models.CharField(max_length=150);icon_awesome=models.TextField(null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
class galery_foto(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);view_count=models.IntegerField(default=0);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(A,*B,**C):A.judul_seo=uuslug(A.judul,instance=A,slug_field=_D,max_length=255);super().save(*B,**C)
class galery_layanan(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);link=models.URLField(max_length=200,null=_A,blank=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
def save_embed_video(embed):
	E='src';D=0;A='';F=embed.split(' ');B=_B
	for G in F:
		if B:break
		H=G.split('=');B=_B
		for C in H:
			if not B and C.lower()==E:B=_A
			if B and C.lower()!=E:
				if D==0:A+=C;D+=1
				else:A+='='+C
				print(A)
	if A.find('watch')<=0:A=A.replace('"','');A=A.replace('&quot;','');return A
	else:return
class galery_video(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);view_count=models.IntegerField(default=0);embed=CKEditor5Field(blank=_A,null=_A,config_name=_C);embed_video=EmbedVideoField(blank=_A,null=_A);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.judul
	def save(A,*B,**C):A.embed_video=save_embed_video(A.embed);super().save(*B,**C)
class instansi_kategori(models.Model):
	nama=models.CharField(max_length=50);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return'{}'.format(A.nama)
class instansi(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ManyToManyField(User,blank=_A);nama=models.CharField(max_length=255);alamat=models.CharField(max_length=255,null=_A,blank=_A);telp=models.CharField(max_length=100,null=_A,blank=_A);email=models.EmailField(max_length=150,null=_A,blank=_A);kode_post=models.CharField(max_length=50,null=_A,blank=_A);kategori=models.ForeignKey(instansi_kategori,null=_A,blank=_A,on_delete=models.PROTECT);parent=models.ForeignKey('self',null=_A,blank=_A,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _F.format(A.site.name,A.nama)
class social_media(models.Model):
	class Jenis(models.TextChoices):FACEBOOK='facebook';TWITTER='twitter';PINTEREST='pinterest';YOUTUBE='youtube';INSTAGRAM='instagram'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);jenis=models.CharField(max_length=20,choices=Jenis.choices,default=Jenis.FACEBOOK);link=models.URLField(max_length=200);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _F.format(A.site.name,A.jenis)
class logo(models.Model):
	class Position(models.TextChoices):TOP='TOP';BOTTOM='BOTTOM'
	site=models.ForeignKey(Site,on_delete=models.CASCADE);photo=models.ForeignKey(photo,on_delete=models.CASCADE,blank=_A);position=models.CharField(max_length=20,choices=Position.choices,default=Position.TOP);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return _F.format(A.site.name,A.position)
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
		return'{} {} > {}'.format(B,C,A.nama)
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
	def get_absolute_url(A):return _E%('halaman statis',A.judul)
class page_widget(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);lokasi=models.CharField(max_length=255);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=CKEditor5Field(blank=_A,null=_A,config_name=_C);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=uuslug(A.nama,instance=A,slug_field=_G,max_length=50);super().save(*B,**C)
class agenda(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);nama=models.CharField(max_length=500);nama_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);deskripsi=CKEditor5Field(blank=_A,null=_A,config_name=_C);lokasi=models.CharField(max_length=30,null=_A,blank=_A);tanggal=models.DateField();jam=models.TimeField();penyelenggara=models.CharField(max_length=100,null=_A,blank=_A);dihadiri_oleh=models.CharField(max_length=100,null=_A,blank=_A);view_count=models.IntegerField(default=0);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=uuslug(A.nama,instance=A,slug_field=_G,max_length=255);super().save(*B,**C)
class page_rss(models.Model):
	site=models.ManyToManyField(Site,blank=_A);nama=models.CharField(max_length=50);nama_seo=models.SlugField(max_length=50,default='',unique=_A,blank=_A);script=CKEditor5Field(blank=_A,null=_A,config_name=_C);admin=models.ForeignKey(User,on_delete=models.PROTECT);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.nama
	def save(A,*B,**C):A.nama_seo=uuslug(A.nama,instance=A,slug_field=_G,max_length=50);super().save(*B,**C)
class popup(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);judul=models.CharField(max_length=500);judul_seo=models.SlugField(max_length=255,default='',unique=_A,blank=_A);link=models.URLField(max_length=200,null=_A,blank=_A);photo=models.ForeignKey(photo,on_delete=models.CASCADE);status=models.CharField(max_length=20,choices=Status.choices,default=Status.PUBLISHED);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.photo
	def save(A,*B,**C):A.judul_seo=uuslug(A.judul,instance=A,slug_field=_D,max_length=255);super().save(*B,**C)
class info_hoax(models.Model):
	name=models.CharField(max_length=100);slug=models.SlugField(max_length=100,default='',unique=_A,blank=_A);link=models.URLField(max_length=200);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
	def save(A,*B,**C):A.slug=uuslug(A.name,instance=A,max_length=100);super().save(*B,**C)
class info_widget(models.Model):
	title=models.CharField(max_length=200);categori=models.CharField(max_length=100);publish_date=models.CharField(max_length=50);author=models.CharField(max_length=50);link=models.URLField(max_length=255);created_at=models.DateTimeField(auto_now_add=_A);updated_at=models.DateTimeField(auto_now=_A)
	def __str__(A):return A.name
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