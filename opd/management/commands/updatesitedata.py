_J='site_group'
_I='halaman_statis'
_H='instansi'
_G='file_path'
_F='site'
_E='m2m'
_D='r'
_C='id'
_B='condition'
_A='defaults'
import sys,os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from opd.models import kategori,photo,tags,menu
import pprint
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_F);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori',_H,'social_media','logo','banner','pejabat',_I,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):sys.stdout.write(message)
	def debug(A,message):sys.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_J,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		A=self;A.info('\nUpdate Site Model ...')
		with open(os.path.join(A.site_list,site_group,'Site.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Site] at {0:.2%}\r'.format(G);A.info(H);I,J=Site.objects.update_or_create(id=D[_B][_C],defaults=D[_A]);C+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		A=self;A.info('\nUpdate User Model ...')
		with open(os.path.join(A.site_list,site_group,'User.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [User] at {0:.2%} '.format(G);A.info(H);I,J=User.objects.get_or_create(id=D[_B][_C],defaults=D[_A]);C+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		A=self;A.info('\nUpdate Photo Model ...')
		with open(os.path.join(A.site_list,site_group,'photo.json'),_D)as E:C=json.load(E)
		D=1;F=len(C)
		for B in C:G=D/F;H='\rWriting Progress [Photo] at {0:.2%} '.format(G);A.info(H);I,J=photo.objects.get_or_create(file_path=B[_A][_G],site_id=B[_A]['site_id'],defaults=B[_A]);D+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		A=self;A.info('\nUpdate Kategori Model ...')
		with open(os.path.join(A.site_list,site_group,'kategori.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Kategori] at {0:.2%} '.format(G);A.info(H);I,J=kategori.objects.get_or_create(id=D[_B][_C],defaults=D[_A]);C+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		A=self;A.info('\nUpdate Tags Model ...')
		with open(os.path.join(A.site_list,site_group,'tags.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Tags] at {0:.2%} '.format(G);A.info(H);I,J=tags.objects.get_or_create(id=D[_B][_C],defaults=D[_A]);C+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		A=self;A.info('\nUpdate Menu Model ...')
		with open(os.path.join(A.site_list,site_group,'menu.json'),_D)as F:D=json.load(F)
		E=1;G=len(D)
		for B in D:
			H=E/G;I='\rWriting Progress [Menu] at {0:.2%} '.format(H);A.info(I);C,L=menu.objects.get_or_create(id=B[_B][_C],defaults=B[_A]);C.site.clear()
			for J in B[_E][_F]:K=Site.objects.get(id=J);C.site.add(K)
			C.save();E+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		h='photo_id';g='menu_id';f='admin';e='photo';d='tags';U=site_group;S='created_at';R=True;Q=False;H=self;G='nama_seo';F='slug';E='judul_seo';H.info('\nUpdate Data By Site ...');V=os.path.join(H.site_list,U);T=[A for A in os.listdir(V)if os.path.isfile(os.path.join(V,A))]
		for K in H.model_list:
			H.info('\nproses model: '+K+'\n')
			for J in range(len(T)):
				L=T[J].split('_');M=L[len(L)-1];M=M.split('.')[:1];M=M[0];L.pop(len(L)-1);W=0;i='_'.join(L)
				if K==i:
					t=None
					with open(os.path.join(H.site_list,U,T[J]),_D)as j:X=json.load(j)
					Y=1;k=len(X)
					for A in X:
						C=apps.get_model('opd',K)
						if C:
							P=0;N=[]
							for I in C._meta.fields:N.append(I.name)
							if _F in N:P=1
							if P==0:
								N=[]
								for I in C._meta.get_fields():N.append(I.name)
								if _F in N:P=2
							Z=Q;a=Q;b=Q;c=Q
							for I in C._meta.get_fields():
								if I.name==E:c=R
								if I.many_to_many:
									if I.name==d:Z=R
									elif I.name==e:a=R
									elif I.name==f:b=R
							if K==_I:
								l=menu.objects.filter(id=A[_A][g])
								if not l:W+=1;H.info('\nSKIP',A[_A][g]);continue
							if K==_H:A[_A].pop('parent_id',None)
							m=Y/k;n='\rWriting Progress [Data Site ID '+str(M)+'] at {0:.2%} '.format(m);H.info(n)
							if h in A[_A]:
								O=photo.objects.filter(file_path=A[_A][_G])[:1]
								if O:
									A[_A].pop(_G);A[_A][h]=O.get().id
									if F in A[_B]:
										B=C.objects.filter(slug=A[_B][F])
										if B:B,D=C.objects.get_or_create(slug=A[_B][F],defaults=A[_A])
										else:B=C.objects.filter(id=A[_A][_C])
										if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(slug=A[_B][F],defaults=A[_A])
										else:B=B.get()
									elif E in A[_B]:
										B=C.objects.filter(judul_seo=A[_B][E])
										if B:B,D=C.objects.get_or_create(judul_seo=A[_B][E],defaults=A[_A])
										else:
											B=C.objects.filter(id=A[_A][_C])
											if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(judul_seo=A[_B][E],defaults=A[_A])
											else:B=B.get()
									elif G in A[_B]:
										B=C.objects.filter(nama_seo=A[_B][G])
										if B:B,D=C.objects.get_or_create(nama_seo=A[_B][G],defaults=A[_A])
										else:
											B=C.objects.filter(id=A[_A][_C])
											if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(nama_seo=A[_B][G],defaults=A[_A])
											else:B=B.get()
									else:B,D=C.objects.get_or_create(id=A[_B][_C],defaults=A[_A])
							elif F in A[_B]:
								B=C.objects.filter(slug=A[_B][F])
								if B:B,D=C.objects.get_or_create(slug=A[_B][F],defaults=A[_A])
								else:
									B=C.objects.filter(id=A[_A][_C])
									if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(slug=A[_B][F],defaults=A[_A])
									else:B=B.get()
							elif E in A[_B]:
								B=C.objects.filter(judul_seo=A[_B][E])
								if B:B,D=C.objects.get_or_create(judul_seo=A[_B][E],defaults=A[_A])
								else:
									B=C.objects.filter(id=A[_A][_C])
									if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(judul_seo=A[_B][E],defaults=A[_A])
									else:B=B.get()
							elif G in A[_B]:
								B=C.objects.filter(nama_seo=A[_B][G])
								if B:B,D=C.objects.get_or_create(nama_seo=A[_B][G],defaults=A[_A])
								else:
									B=C.objects.filter(id=A[_A][_C])
									if not B:A[_A].pop(_C);B,D=C.objects.get_or_create(nama_seo=A[_B][G],defaults=A[_A])
									else:B=B.get()
							else:B,D=C.objects.get_or_create(id=A[_B][_C],defaults=A[_A])
							if Z:
								B.tags.clear()
								for J in A[_E][d]:o=tags.objects.get(id=J);B.tags.add(o)
								B.save()
							if a:
								B.photo.clear()
								for J in A[_E][e]:
									O=photo.objects.filter(file_path=J)[:1]
									if O:p=O.get();B.photo.add(p)
								B.save()
							if b:
								B.admin.clear()
								for J in A[_E][f]:q=User.objects.get(id=J);B.admin.add(q)
								B.save()
							if P==2:
								if _E in A:
									if _F in A[_E]:
										B.site.clear()
										for r in A[_E][_F]:s=Site.objects.get(id=r);B.site.add(s)
										B.save()
							if c:
								if F in A[_B]:C.objects.filter(slug=A[_B][F]).update(slug=A[_B][F],created_at=A[_A][S])
								elif E in A[_B]:C.objects.filter(judul_seo=A[_B][E]).update(judul_seo=A[_B][E],created_at=A[_A][S])
								elif G in A[_B]:C.objects.filter(nama_seo=A[_B][G]).update(nama_seo=A[_B][G],created_at=A[_A][S])
								else:C.objects.filter(id=A[_B][_C]).update(created_at=A[_A][S])
							Y+=1
					H.info('\n')
			H.info('\nSKIP '+str(W))
	def handle(A,*F,**C):
		A.info('Begin get site data\n');B=C[_J];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_site_model(B);A.update_user_model(B);A.update_kategori_model(B);A.update_tags_model(B);A.update_menu_model(B);A.update_photo_model(B);A.update_data_by_site(B)
		else:A.info('\ndb_name NOT MATCH:')
		A.info('\nEnd get site data\n')