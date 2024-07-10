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
		with open(os.path.join(self.site_list,site_group,'menu.json'),'r')as D:B=json.load(D)
		C=1;E=len(B)
		for A in B:F=C/E*100;print('ID-menu',A[_B][_C]);print(f"Writing [menu Default] to database [%d%%]\r"%F,end='');G,H=menu.objects.update_or_create(id=A[_B][_C],defaults=A[_A]);C+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		U='m2m';T='menu_id';S='tags';R=False;L=site_group;G=self;print('Update Site Data ...');M=os.path.join(G.site_list,L);H=[A for A in os.listdir(M)if os.path.isfile(os.path.join(M,A))]
		for E in G.model_list:
			print('proses model: ',E)
			for A in range(len(H)):
				D=H[A].split('_');F=D[len(D)-1];F=F.split('.')[:1];F=F[0];D.pop(len(D)-1);N=0;V='_'.join(D)
				if E==V:
					c=None
					with open(os.path.join(G.site_list,L,H[A]),'r')as W:O=json.load(W)
					I=1;X=len(O)
					for B in O:
						J=apps.get_model('opd',E)
						if J:
							P=R;Q=R
							for K in J._meta.get_fields():
								if K.many_to_many:
									if K.name==S:P=True
									elif K.name==_D:Q=True
							if E==_E:
								Y=menu.objects.filter(id=B[_A][T])
								if not Y:N+=1;I+=1;print('SKIP',B[_A][T]);continue
							Z=I/X*100;print(f"Writing [Site Default] to database [%d%%]\r"%Z,end='');C,d=J.objects.update_or_create(id=B[_B][_C],defaults=B[_A])
							if P:
								C.tags.clear()
								for A in B[U][S]:a=tags.objects.get(id=A);C.tags.add(a)
								C.save()
							if Q:
								C.photo.clear()
								for A in B[U][_D]:b=photo.objects.get(id=A);C.photo.add(b)
								C.save()
							I+=1
			print('SKIP:',N)
	def handle(A,*F,**B):
		A.info('Begin get site data');C=B[_F];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_data_by_site(C)
		else:print('db_name NOT MATCH:')
		A.info('End get site data')