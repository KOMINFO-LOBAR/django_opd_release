_Q='proses model: '
_P='Update Site Data ...'
_O='site_group'
_N='instansi'
_M='halaman_statis'
_L='menu_id'
_K='admin'
_J='photo'
_I='tags'
_H='photo_id'
_G=True
_F=False
_E='m2m'
_D='r'
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
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,'site');photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori',_N,'social_media','logo','banner','pejabat',_M,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_O,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		print('Update Site Model ...')
		with open(os.path.join(self.site_list,site_group,'Site.json'),_D)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [Site] to database [%d%%]\r"%F,end='');G,H=Site.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		print('Update User Model ...')
		with open(os.path.join(self.site_list,site_group,'User.json'),_D)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [User] to database [%d%%]\r"%F,end='');G,H=User.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		print('Update Photo Model ...')
		with open(os.path.join(self.site_list,site_group,'photo.json'),_D)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [photo] to database [%d%%]\r"%F,end='');G,H=photo.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		print('Update Kategori Model ...')
		with open(os.path.join(self.site_list,site_group,'kategori.json'),_D)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [kategori] to database [%d%%]\r"%F,end='');G,H=kategori.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		print('Update Tags Model ...')
		with open(os.path.join(self.site_list,site_group,'tags.json'),_D)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;print(f"Writing [tags] to database [%d%%]\r"%F,end='');G,H=tags.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		print('Update Menu Model ...')
		with open(os.path.join(self.site_list,site_group,'menu.json'),_D)as E:C=json.load(E)
		D=1;F=len(C)
		for A in C:
			G=D/F*100;print(f"Writing [menu] to database [%d%%]\r"%G,end='');B,J=menu.objects.update_or_create(id=A[_B][_C],defaults=A[_A]);B.site.clear()
			for H in A[_E]['site']:I=Site.objects.get(id=H);B.site.add(I)
			B.save();D+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		M=site_group;I=self;print(_P);N=os.path.join(I.site_list,M);J=[A for A in os.listdir(N)if os.path.isfile(os.path.join(N,A))]
		for D in I.model_list:
			print(_Q,D)
			for C in range(len(J)):
				E=J[C].split('_');F=E[len(E)-1];F=F.split('.')[:1];F=F[0];E.pop(len(E)-1);O=0;T='_'.join(E)
				if D==T:
					c=None
					with open(os.path.join(I.site_list,M,J[C]),_D)as U:P=json.load(U)
					K=1;V=len(P)
					for A in P:
						G=apps.get_model('opd',D)
						if G:
							Q=_F;R=_F;S=_F
							for H in G._meta.get_fields():
								if H.many_to_many:
									if H.name==_I:Q=_G
									elif H.name==_J:R=_G
									elif H.name==_K:S=_G
							if D==_M:
								W=menu.objects.filter(id=A[_A][_L])
								if not W:O+=1;K+=1;print('SKIP',A[_A][_L]);continue
							if D==_N:A[_A].pop('parent_id',None)
							X=K/V*100;print(f"Writing [{D}] - Site [{F}] to database [%d%%]\r"%X,end='')
							if _H in A[_A]:
								L=photo.objects.filter(id=A[_A][_H])
								if L:B,Y=G.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							else:B,Y=G.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							if Q:
								B.tags.clear()
								for C in A[_E][_I]:Z=tags.objects.get(id=C);B.tags.add(Z)
								B.save()
							if R:
								B.photo.clear()
								for C in A[_E][_J]:
									L=photo.objects.filter(id=C)
									if L:a=photo.objects.get(id=C);B.photo.add(a)
								B.save()
							if S:
								B.admin.clear()
								for C in A[_E][_K]:b=User.objects.get(id=C);B.admin.add(b)
								B.save()
							K+=1
			print('SKIP:',O)
	@transaction.atomic
	def update_data_by_site_old(self,site_group):
		W='-----';M=site_group;J=self;print(_P);N=os.path.join(J.site_list,M);K=[A for A in os.listdir(N)if os.path.isfile(os.path.join(N,A))]
		for F in J.model_list:
			print(_Q,F)
			for O in range(len(K)):
				D=K[O].split('_');G=D[len(D)-1];G=G.split('.')[:1];G=G[0];D.pop(len(D)-1);P=0;Q='_'.join(D);print('compare',Q)
				if F==Q:
					f=None
					with open(os.path.join(J.site_list,M,K[O]),_D)as X:R=json.load(X)
					L=1;Y=len(R)
					for A in R:
						C=apps.get_model('opd',F);print(W);print('i=====',C.__name__);print(W)
						if C:
							S=_F;T=_F;U=_F
							for H in C._meta.get_fields():
								if H.many_to_many:
									if H.name==_I:S=_G
									elif H.name==_J:T=_G
									elif H.name==_K:U=_G
							if F==_M:
								Z=menu.objects.filter(id=A[_A][_L])
								if not Z:P+=1;L+=1;print('SKIP',A[_A][_L]);continue
							a=L/Y*100;print(f"Writing {C.__name__} to database [%d%%]\r"%a,end='')
							if _H in A[_A]:
								I=photo.objects.filter(id=A[_A][_H])
								if I:B,b=C.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
								else:print('SKIP [Photo ID Not Found]',A[_A][_H])
							else:B,b=C.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							if S:
								B.tags.clear()
								for E in A[_E][_I]:c=tags.objects.get(id=E);B.tags.add(c)
								B.save()
							if T:
								B.photo.clear();V=_F
								for E in A[_E][_J]:
									I=photo.objects.filter(id=E)
									if I:d=I.get();B.photo.add(d);V=_G
								if V:B.save()
							if U:
								B.admin.clear()
								for E in A[_E][_K]:e=User.objects.get(id=E);B.admin.add(e)
								B.save()
							L+=1
			print('SKIP:',P)
	def handle(A,*F,**C):
		A.info('Begin get site data');B=C[_O];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_site_model(B);A.update_user_model(B);A.update_kategori_model(B);A.update_tags_model(B);A.update_menu_model(B);A.update_photo_model(B);A.update_data_by_site(B)
		else:print('db_name NOT MATCH:')
		A.info('End get site data')