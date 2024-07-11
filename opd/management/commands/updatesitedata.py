_F='site_group'
_E='halaman_statis'
_D='photo'
_C='id'
_B='condition'
_A='defaults'
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from opd.models import kategori,photo,tags,menu
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,'site');photo_dir=os.path.join(base_dir,'media','images');model_list=[_D,'berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','pejabat',_E,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_F,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		print('Update Site Model ...')
		with open(os.path.join(self.site_list,site_group,'Site.json'),'r')as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [Site Default] to database [%d%%]\r"%F,end='');G,H=Site.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		print('Update User Model ...')
		with open(os.path.join(self.site_list,site_group,'User.json'),'r')as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [User Default] to database [%d%%]\r"%F,end='');G,H=User.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		print('Update Kategori Model ...')
		with open(os.path.join(self.site_list,site_group,'kategori.json'),'r')as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [kategori Default] to database [%d%%]\r"%F,end='');G,H=kategori.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		print('Update Tags Model ...')
		with open(os.path.join(self.site_list,site_group,'tags.json'),'r')as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [tags Default] to database [%d%%]\r"%F,end='');G,H=tags.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		print('Update Menu Model ...')
		with open(os.path.join(self.site_list,site_group,'menu.json'),'r')as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [menu Default] to database [%d%%]\r"%F,end='');G,H=menu.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		U='m2m';T='menu_id';S='tags';R=False;M=site_group;H=self;print('Update Site Data ...');I=os.path.join(H.site_list,M);print('source_folder',I);D=[A for A in os.listdir(I)if os.path.isfile(os.path.join(I,A))];print('source_file',D,len(D))
		for F in H.model_list:
			print('proses model: ',F)
			for A in range(len(D)):
				E=D[A].split('_');G=E[len(E)-1];G=G.split('.')[:1];G=G[0];E.pop(len(E)-1);N=0;V='_'.join(E)
				if F==V:
					c=None
					with open(os.path.join(H.site_list,M,D[A]),'r')as W:O=json.load(W)
					J=1;X=len(O)
					for B in O:
						K=apps.get_model('opd',F)
						if K:
							P=R;Q=R
							for L in K._meta.get_fields():
								if L.many_to_many:
									if L.name==S:P=True
									elif L.name==_D:Q=True
							if F==_E:
								Y=menu.objects.filter(id=B[_A][T])
								if not Y:N+=1;J+=1;print('SKIP',B[_A][T]);continue
							Z=J/X*100;print(f"Writing [Site Default] to database [%d%%]\r"%Z,end='');C,d=K.objects.update_or_create(id=B[_B][_C],defaults=B[_A])
							if P:
								C.tags.clear()
								for A in B[U][S]:a=tags.objects.get(id=A);C.tags.add(a)
								C.save()
							if Q:
								C.photo.clear()
								for A in B[U][_D]:b=photo.objects.get(id=A);C.photo.add(b)
								C.save()
							J+=1
			print('SKIP:',N)
	def handle(A,*F,**B):
		A.info('Begin get site data');C=B[_F];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_data_by_site(C)
		else:print('db_name NOT MATCH:')
		A.info('End get site data')