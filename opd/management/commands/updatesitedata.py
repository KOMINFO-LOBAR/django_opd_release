_F='site_group'
_E='halaman_statis'
_D='id'
_C='condition'
_B='r'
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
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,'site');photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','pejabat',_E,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_F,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		print('Update Site Model ...')
		with open(os.path.join(self.site_list,site_group,'Site.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [Site Default] to database [%d%%]\r"%F,end='');G,H=Site.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		print('Update User Model ...')
		with open(os.path.join(self.site_list,site_group,'User.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [User Default] to database [%d%%]\r"%F,end='');G,H=User.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		print('Update Photo Model ...')
		with open(os.path.join(self.site_list,site_group,'photo.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [photo Default] to database [%d%%]\r"%F,end='');G,H=photo.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		print('Update Kategori Model ...')
		with open(os.path.join(self.site_list,site_group,'kategori.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [kategori Default] to database [%d%%]\r"%F,end='');G,H=kategori.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		print('Update Tags Model ...')
		with open(os.path.join(self.site_list,site_group,'tags.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [tags Default] to database [%d%%]\r"%F,end='');G,H=tags.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		print('Update Menu Model ...')
		with open(os.path.join(self.site_list,site_group,'menu.json'),_B)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [menu Default] to database [%d%%]\r"%F,end='');G,H=menu.objects.update_or_create(id=C[_C][_D],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		Y='menu_id';X='admin';W='photo';V='tags';P=site_group;O='m2m';N=True;M=False;I=self;print('Update Site Data ...');J=os.path.join(I.site_list,P);print('source_folder',J);D=[A for A in os.listdir(J)if os.path.isfile(os.path.join(J,A))];print('source_file',D,len(D))
		for F in I.model_list:
			print('proses model: ',F)
			for B in range(len(D)):
				E=D[B].split('_');G=E[len(E)-1];G=G.split('.')[:1];G=G[0];E.pop(len(E)-1);Q=0;Z='_'.join(E)
				if F==Z:
					h=None
					with open(os.path.join(I.site_list,P,D[B]),_B)as a:R=json.load(a)
					K=1;b=len(R)
					for C in R:
						L=apps.get_model('opd',F)
						if L:
							S=M;T=M;U=M
							for H in L._meta.get_fields():
								if H.many_to_many:
									if H.name==V:S=N
									elif H.name==W:T=N
									elif H.name==X:U=N
							if F==_E:
								c=menu.objects.filter(id=C[_A][Y])
								if not c:Q+=1;K+=1;print('SKIP',C[_A][Y]);continue
							d=K/b*100;print(f"Writing [Site Default] to database [%d%%]\r"%d,end='');A,i=L.objects.update_or_create(id=C[_C][_D],defaults=C[_A])
							if S:
								A.tags.clear()
								for B in C[O][V]:e=tags.objects.get(id=B);A.tags.add(e)
								A.save()
							if T:
								A.photo.clear()
								for B in C[O][W]:f=photo.objects.get(id=B);A.photo.add(f)
								A.save()
							if U:
								A.admin.clear()
								for B in C[O][X]:g=User.objects.get(id=B);A.admin.add(g)
								A.save()
							K+=1
			print('SKIP:',Q)
	def handle(A,*F,**C):
		A.info('Begin get site data');B=C[_F];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_site_model(B);A.update_user_model(B);A.update_kategori_model(B);A.update_tags_model(B);A.update_menu_model(B);A.update_photo_model(B);A.update_data_by_site(B)
		else:print('db_name NOT MATCH:')
		A.info('End get site data')