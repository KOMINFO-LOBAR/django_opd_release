import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,'site');photo_dir=os.path.join(base_dir,'media','images');model_list=['photo','kategori','tags','berita','comment','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','menu','pejabat','halaman_statis','agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def update_data_by_site(E):
		print('Update Site Data ...');F=[A.split('_')[len(A.split('_'))-1]for A in list_file];E.info('res_folder: ['+', '.join(F)+']');A=[]
		with open(os.path.join(file_path,'social_app.json'),'r')as G:A=json.load(G)
		B=1;C=len(A)
		for D in A:H=B/C*100;print(f"Writing [Social App] to database [%d%%]\r"%H,end='');I,J=SocialApp.objects.update_or_create(id=D['condition']['id'],defaults=D['defaults']);B+=1
		print(f"Writing [Social App] to database ({C} data) {color_done}")
	def handle(A,*B,**C):A.info('Begin get site data');A.update_data_by_site();A.info('End get site data')