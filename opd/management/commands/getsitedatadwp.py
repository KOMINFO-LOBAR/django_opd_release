_H='thumbnail'
_G='nama'
_F='url'
_E='slug'
_D='Asia/Makassar'
_C='name'
_B='updated_at'
_A='created_at'
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from opd.models import*
from django.db import transaction
import pytz
class Command(BaseCommand):
	help='Get Site Data Specific for DWP'
	def info(self,message):sys.stdout.write(message)
	def debug(self,message):sys.stdout.write(message)
	@transaction.atomic
	def create_site(self):obj,created=Site.objects.get_or_create(domain='dwp.lombokbaratkab.go.id',defaults={_C:'DWP'});return obj
	@transaction.atomic
	def create_user(self):
		A='dwplobar';user=User.objects.filter(username=A)
		if user:return user.get()
		user=User.objects.create_user(A,'dwpkablombokbarat@gmail.com','dwp60175410');return user
	def get_data(self,table_name,opt_where='',opt_query=''):
		with connections['second_db'].cursor()as cursor:
			if opt_query:sql_string=opt_query
			elif opt_where:sql_string=f"SELECT * FROM {table_name} WHERE {opt_where}"
			else:sql_string=f"SELECT * FROM {table_name}"
			cursor.execute(sql_string);dat=cursor.fetchall();desc=cursor.description;data_dic=[dict(zip([col[0]for col in desc],row))for row in dat];return data_dic
	@transaction.atomic
	def create_instansi(self,site,user):
		A='email';timezone=pytz.timezone(_D);table_name='app_settings';app_settings=self.get_data(table_name);mlist=[]
		for i in range(len(app_settings)):tmp=app_settings[i];condition={_G:tmp[_C],'site':site};defaults={};defaults['alamat']=tmp['address'];defaults['telp']=tmp['phone'];defaults[A]=tmp[A];defaults[_A]=timezone.localize(tmp[_A]);defaults[_B]=timezone.localize(tmp[_B]);obj,created=instansi.objects.update_or_create(nama=tmp[_C],site=site,defaults=defaults);obj.admin.add(user);obj.save();instansi.objects.filter(nama=tmp[_C],site=site).update(created_at=timezone.localize(tmp[_A]))
	@transaction.atomic
	def create_banner(self,site):
		A='position';timezone=pytz.timezone(_D);table_name='banners';app_model=self.get_data(table_name);mlist=[]
		for i in range(len(app_model)):
			tmp=app_model[i]
			if tmp[A]=='top':obj_photo,created=photo.objects.update_or_create(site=site,jenis=photo.Jenis.BANNER_TOP,defaults={'file_path':tmp[_H]});obj,created=banner.objects.update_or_create(position=tmp[A],site=site,defaults={'link':tmp[_F],'photo':obj_photo,_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])});banner.objects.filter(position=tmp[A],site=site).update(created_at=timezone.localize(tmp[_A]))
	@transaction.atomic
	def create_kategori(self,site):
		timezone=pytz.timezone(_D);table_name='categories';app_model=self.get_data(table_name);mlist=[]
		for i in range(len(app_model)):tmp=app_model[i];obj,created=kategori.objects.update_or_create(slug=tmp[_E],site__id=site.id,defaults={_G:tmp[_C],_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])});obj.site.add(site);obj.save();kategori.objects.filter(slug=tmp[_E],site__id=site.id).update(created_at=timezone.localize(tmp[_A]));obj_tag,created=tags.objects.update_or_create(nama=tmp[_C],site__id=site.id,defaults={_E:tmp[_E],_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])});obj_tag.site.add(site);obj_tag.save();tags.objects.filter(nama=tmp[_C],site__id=site.id).update(created_at=timezone.localize(tmp[_A]))
	@transaction.atomic
	def create_berita(self,site,user):
		timezone=pytz.timezone(_D);table_name='news';app_model=self.get_data(table_name);cat_news_default,created=kategori.objects.get_or_create(slug='berita-utama',site__id=site.id,defaults={_G:'Berita Utama'});self.info('\n');mlist=[];lendata=len(app_model)
		for i in range(lendata):
			tmp=app_model[i];tmp_count=(i+1)/lendata;time_msg='\rWriting Progress [Data] at {0:.2%} '.format(tmp_count);self.info(time_msg);obj_photo,created=photo.objects.get_or_create(site_id=site.id,jenis=photo.Jenis.HIGHLIGHT1,file_path=tmp[_H]);sql_='SELECT news.id, news.title, category_news.category_id, categories.name FROM  ';sql_=sql_+'news INNER JOIN  category_news ON news.id = category_news.news_id INNER JOIN ';sql_=sql_+'categories ON category_news.category_id = categories.id WHERE news.slug=';sql_=sql_+'"'+str(tmp[_E])+'"';sql_=sql_+' order by news.id;';app_model_cat=self.get_data(table_name=None,opt_query=sql_);cat_name=[]
			for j in range(len(app_model_cat)):tmp_cat=app_model_cat[j];cat_name.append(tmp_cat[_C])
			m_status=Status.DRAFT
			if tmp['drafted']=='Tidak':m_status=Status.PUBLISHED
			cat_name_0=None
			if len(cat_name)>0:
				cat_name_0=kategori.objects.filter(site__id=site.id,nama=cat_name[0])[:1]
				if cat_name_0:cat_name_0=cat_name_0.get()
			obj,created=berita.objects.update_or_create(judul=tmp['title'],site_id=site.id,defaults={'judul_seo':tmp[_E],'status':m_status,'admin_id':user.id,'kategori_id':cat_name_0.id if cat_name_0 else cat_news_default.id,'isi_berita':tmp['content'],'view_count':tmp['viewed'],_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])})
			if created:pass
			else:pass
			obj.photo.clear();obj.photo.add(obj_photo);obj.tags.clear()
			for j in range(len(cat_name)):
				cat_name_0=tags.objects.filter(site__id=site.id,nama=cat_name[j])[:1]
				if cat_name_0:cat_name_0=cat_name_0.get();obj.tags.add(cat_name_0)
			obj.save();obj=berita.objects.filter(id=obj.id);obj.update(created_at=timezone.localize(tmp[_A]));
	@transaction.atomic
	def create_related_link(self,site):
		timezone=pytz.timezone(_D);table_name='related_links';app_model=self.get_data(table_name)
		for i in range(len(app_model)):tmp=app_model[i];obj,created=link_terkait.objects.update_or_create(site__id=site.id,link=tmp[_F],defaults={_G:tmp[_C],_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])});obj.site.add(site);obj.save();obj=link_terkait.objects.filter(site__id=site.id,link=tmp[_F]);obj.update(created_at=timezone.localize(tmp[_A]))
	@transaction.atomic
	def create_social_media(self,site):
		timezone=pytz.timezone(_D);table_name='social_medias';app_model=self.get_data(table_name)
		for i in range(len(app_model)):tmp=app_model[i];obj,created=social_media.objects.update_or_create(site_id=site.id,link=tmp[_F],defaults={'jenis':tmp[_C],_A:timezone.localize(tmp[_A]),_B:timezone.localize(tmp[_B])});obj=social_media.objects.filter(site_id=site.id,link=tmp[_F]);obj.update(created_at=timezone.localize(tmp[_A]))
	def handle(self,*args,**options):self.info('\n---Begin get DWP Data---');self.info('\nCreate Site');site=self.create_site();self.info('\nCreate User');user=self.create_user();self.info('\nCreate Instansi');self.create_instansi(site,user);self.info('\nCreate Banner');self.create_banner(site);self.info('\nCreate Categories');self.create_kategori(site);self.info('\nCreate News');self.create_berita(site,user);self.info('\nCreate Related Link');self.create_related_link(site);self.info('\nCreate Social Media');self.create_social_media(site);self.info('\n---End get DWP Data---\n')