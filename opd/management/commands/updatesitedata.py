_S='proses model: '
_R='Update Site Data ...'
_Q='site_group'
_P='instansi'
_O='SKIP'
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
_B='defaults'
_A='condition'
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
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_H);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori',_P,'social_media','logo','banner','pejabat',_N,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message);A.stdout.flush()
	def debug(A,message):A.stdout.write(message);A.stdout.flush()
	def add_arguments(A,parser):parser.add_argument(_Q,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'Site.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E;G='\rWriting Progress [Site] at {0:.2%}\r'.format(F);self.info(G);H,I=Site.objects.update_or_create(id=C[_A][_C],defaults=C[_B]);B+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'User.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E;G='\rWriting Progress [User] at {0:.2%} '.format(F);self.info(G);H,I=User.objects.update_or_create(id=C[_A][_C],defaults=C[_B]);B+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'photo.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E;G='\rWriting Progress [Photo] at {0:.2%} '.format(F);self.info(G);H,I=photo.objects.update_or_create(id=C[_A][_C],defaults=C[_B]);B+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'kategori.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E;G='\rWriting Progress [Kategori] at {0:.2%} '.format(F);self.info(G);H,I=kategori.objects.update_or_create(id=C[_A][_C],defaults=C[_B]);B+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'tags.json'),_E)as D:A=json.load(D)
		B=1;E=len(A)
		for C in A:F=B/E;G='\rWriting Progress [Tags] at {0:.2%} '.format(F);self.info(G);H,I=tags.objects.update_or_create(id=C[_A][_C],defaults=C[_B]);B+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		with open(os.path.join(self.site_list,site_group,'menu.json'),_E)as E:C=json.load(E)
		D=1;F=len(C)
		for A in C:
			G=D/F;H='\rWriting Progress [Menu] at {0:.2%} '.format(G);self.info(H);B,K=menu.objects.update_or_create(id=A[_A][_C],defaults=A[_B]);B.site.clear()
			for I in A[_D][_H]:J=Site.objects.get(id=I);B.site.add(J)
			B.save();D+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		S=site_group;P='created_at';J=self;I='nama_seo';H='slug';F='judul_seo';T=os.path.join(J.site_list,S);Q=[A for A in os.listdir(T)if os.path.isfile(os.path.join(T,A))]
		for K in J.model_list:
			for D in range(len(Q)):
				L=Q[D].split('_');N=L[len(L)-1];N=N.split('.')[:1];N=N[0];L.pop(len(L)-1);a=0;b='_'.join(L)
				if K==b:
					m=None
					with open(os.path.join(J.site_list,S,Q[D]),_E)as c:U=json.load(c)
					V=1;d=len(U)
					for A in U:
						C=apps.get_model('opd',K)
						if C:
							O=0;M=[]
							for E in C._meta.fields:M.append(E.name)
							if _H in M:O=1
							if O==0:
								M=[]
								for E in C._meta.get_fields():M.append(E.name)
								if _H in M:O=2
							W=_F;X=_F;Y=_F;Z=_F
							for E in C._meta.get_fields():
								if E.name==F:Z=_G
								if E.many_to_many:
									if E.name==_J:W=_G
									elif E.name==_K:X=_G
									elif E.name==_L:Y=_G
							if K==_N:
								e=menu.objects.filter(id=A[_B][_M])
								if not e:a+=1;continue
							if K==_P:A[_B].pop('parent_id',None)
							f=V/d;g='\rWriting Progress [Data] at {0:.2%} '.format(f);J.info(g)
							if _I in A[_B]:
								R=photo.objects.filter(id=A[_B][_I])
								if R:
									if H in A[_A]:B,G=C.objects.update_or_create(slug=A[_A][H],defaults=A[_B])
									elif F in A[_A]:B,G=C.objects.update_or_create(judul_seo=A[_A][F],defaults=A[_B])
									elif I in A[_A]:B,G=C.objects.update_or_create(nama_seo=A[_A][I],defaults=A[_B])
									else:B,G=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
							elif H in A[_A]:B,G=C.objects.update_or_create(slug=A[_A][H],defaults=A[_B])
							elif F in A[_A]:B,G=C.objects.update_or_create(judul_seo=A[_A][F],defaults=A[_B])
							elif I in A[_A]:B,G=C.objects.update_or_create(nama_seo=A[_A][I],defaults=A[_B])
							else:B,G=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
							if W:
								B.tags.clear()
								for D in A[_D][_J]:h=tags.objects.get(id=D);B.tags.add(h)
								B.save()
							if X:
								B.photo.clear()
								for D in A[_D][_K]:
									R=photo.objects.filter(id=D)
									if R:i=photo.objects.get(id=D);B.photo.add(i)
								B.save()
							if Y:
								B.admin.clear()
								for D in A[_D][_L]:j=User.objects.get(id=D);B.admin.add(j)
								B.save()
							if O==2:
								if _D in A:
									if _H in A[_D]:
										B.site.clear()
										for k in A[_D][_H]:l=Site.objects.get(id=k);B.site.add(l)
										B.save()
							if Z:
								if H in A[_A]:C.objects.filter(slug=A[_A][H]).update(slug=A[_A][H],created_at=A[_B][P])
								elif F in A[_A]:C.objects.filter(judul_seo=A[_A][F]).update(judul_seo=A[_A][F],created_at=A[_B][P])
								elif I in A[_A]:C.objects.filter(nama_seo=A[_A][I]).update(nama_seo=A[_A][I],created_at=A[_B][P])
								else:C.objects.filter(id=A[_A][_C]).update(created_at=A[_B][P])
							V+=1
			J.info(_O)
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
								Z=menu.objects.filter(id=A[_B][_M])
								if not Z:P+=1;L+=1;continue
							a=L/Y;
							if _I in A[_B]:
								I=photo.objects.filter(id=A[_B][_I])
								if I:B,b=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
								else:pass
							else:B,b=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
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
	def handle(A,*G,**D):
		C='\n';A.info('Begin get site data');B=D[_Q];E=input('Confirm DB Name: ');F=settings.DATABASES
		if E==F['default']['NAME']:A.update_site_model(B);A.info(C);A.update_user_model(B);A.info(C);A.update_kategori_model(B);A.info(C);A.update_tags_model(B);A.info(C);A.update_menu_model(B);A.info(C);A.update_photo_model(B);A.info(C);A.update_data_by_site(B);A.info(C)
		else:A.info('db_name NOT MATCH:')
		A.info('End get site data')