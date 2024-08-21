_R='proses model: '
_Q='Update Site Data ...'
_P='site_group'
_O='instansi'
_N='halaman_statis'
_M='menu_id'
_L='admin'
_K='photo'
_J='tags'
_I='photo_id'
_H='site'
_G=True
_F=False
_E='r'
_D='m2m'
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
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_H);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori',_O,'social_media','logo','banner','pejabat',_N,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_P,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'Site.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;G,H=Site.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'User.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;G,H=User.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'photo.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;G,H=photo.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'kategori.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;G,H=kategori.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'tags.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E*100;G,H=tags.objects.update_or_create(id=C[_B][_C],defaults=C[_A]);B+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'menu.json'),_E)as E:C=json.load(E)
		D=1;F=len(C)
		for A in C:
			G=D/F*100;B,J=menu.objects.update_or_create(id=A[_B][_C],defaults=A[_A]);B.site.clear()
			for H in A[_D][_H]:I=Site.objects.get(id=H);B.site.add(I)
			B.save();D+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		O=site_group;K=self;P=os.path.join(K.site_list,O);L=[A for A in os.listdir(P)if os.path.isfile(os.path.join(P,A))]
		for E in K.model_list:
			for C in range(len(L)):
				G=L[C].split('_');H=G[len(G)-1];H=H.split('.')[:1];H=H[0];G.pop(len(G)-1);Q=0;V='_'.join(G)
				if E==V:
					g=None
					with open(os.path.join(K.site_list,O,L[C]),_E)as W:R=json.load(W)
					M=1;X=len(R)
					for A in R:
						F=apps.get_model('opd',E)
						if F:
							J=0;I=[]
							for D in F._meta.fields:I.append(D.name)
							if _H in I:J=1
							if J==0:
								I=[]
								for D in F._meta.get_fields():I.append(D.name)
								if _H in I:J=2
							S=_F;T=_F;U=_F
							for D in F._meta.get_fields():
								if D.many_to_many:
									if D.name==_J:S=_G
									elif D.name==_K:T=_G
									elif D.name==_L:U=_G
							if E==_N:
								Y=menu.objects.filter(id=A[_A][_M])
								if not Y:Q+=1;M+=1;continue
							if E==_O:A[_A].pop('parent_id',None)
							Z=M/X*100;
							if _I in A[_A]:
								N=photo.objects.filter(id=A[_A][_I])
								if N:B,a=F.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							else:B,a=F.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							if S:
								B.tags.clear()
								for C in A[_D][_J]:b=tags.objects.get(id=C);B.tags.add(b)
								B.save()
							if T:
								B.photo.clear()
								for C in A[_D][_K]:
									N=photo.objects.filter(id=C)
									if N:c=photo.objects.get(id=C);B.photo.add(c)
								B.save()
							if U:
								B.admin.clear()
								for C in A[_D][_L]:d=User.objects.get(id=C);B.admin.add(d)
								B.save()
							if J==2:
								if _D in A:
									if _H in A[_D]:
										B.site.clear()
										for e in A[_D][_H]:f=Site.objects.get(id=e);B.site.add(f)
										B.save()
							M+=1
	@transaction.atomic
	def update_data_by_site_old(self,site_group):
		W='-----';M=site_group;J=self;N=os.path.join(J.site_list,M);K=[A for A in os.listdir(N)if os.path.isfile(os.path.join(N,A))]
		for F in J.model_list:
			for O in range(len(K)):
				D=K[O].split('_');G=D[len(D)-1];G=G.split('.')[:1];G=G[0];D.pop(len(D)-1);P=0;Q='_'.join(D);
				if F==Q:
					f=None
					with open(os.path.join(J.site_list,M,K[O]),_E)as X:R=json.load(X)
					L=1;Y=len(R)
					for A in R:
						C=apps.get_model('opd',F);
						if C:
							S=_F;T=_F;U=_F
							for H in C._meta.get_fields():
								if H.many_to_many:
									if H.name==_J:S=_G
									elif H.name==_K:T=_G
									elif H.name==_L:U=_G
							if F==_N:
								Z=menu.objects.filter(id=A[_A][_M])
								if not Z:P+=1;L+=1;continue
							a=L/Y*100;
							if _I in A[_A]:
								I=photo.objects.filter(id=A[_A][_I])
								if I:B,b=C.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
								else:pass
							else:B,b=C.objects.update_or_create(id=A[_B][_C],defaults=A[_A])
							if S:
								B.tags.clear()
								for E in A[_D][_J]:c=tags.objects.get(id=E);B.tags.add(c)
								B.save()
							if T:
								B.photo.clear();V=_F
								for E in A[_D][_K]:
									I=photo.objects.filter(id=E)
									if I:d=I.get();B.photo.add(d);V=_G
								if V:B.save()
							if U:
								B.admin.clear()
								for E in A[_D][_L]:e=User.objects.get(id=E);B.admin.add(e)
								B.save()
							L+=1
	def handle(A,*F,**C):
		A.info('Begin get site data');B=C[_P];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_site_model(B);A.update_user_model(B);A.update_kategori_model(B);A.update_tags_model(B);A.update_menu_model(B);A.update_photo_model(B);A.update_data_by_site(B)
		else:pass
		A.info('End get site data')