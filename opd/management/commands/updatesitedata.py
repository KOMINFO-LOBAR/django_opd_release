_I='site_group'
_H='halaman_statis'
_G='instansi'
_F='site'
_E='m2m'
_D='r'
_C='id'
_B='defaults'
_A='condition'
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
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_F);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori',_G,'social_media','logo','banner','pejabat',_H,'agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):sys.stdout.write(message)
	def debug(A,message):sys.stdout.write(message)
	def add_arguments(A,parser):parser.add_argument(_I,type=str)
	@transaction.atomic
	def update_site_model(self,site_group):
		A=self;A.info('\nUpdate Site Model ...')
		with open(os.path.join(A.site_list,site_group,'Site.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Site] at {0:.2%}\r'.format(G);A.info(H);I,J=Site.objects.update_or_create(id=D[_A][_C],defaults=D[_B]);C+=1
	@transaction.atomic
	def update_user_model(self,site_group):
		A=self;A.info('\nUpdate User Model ...')
		with open(os.path.join(A.site_list,site_group,'User.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [User] at {0:.2%} '.format(G);A.info(H);I,J=User.objects.update_or_create(id=D[_A][_C],defaults=D[_B]);C+=1
	@transaction.atomic
	def update_photo_model(self,site_group):
		A=self;A.info('\nUpdate Photo Model ...')
		with open(os.path.join(A.site_list,site_group,'photo.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Photo] at {0:.2%} '.format(G);A.info(H);I,J=photo.objects.update_or_create(id=D[_A][_C],defaults=D[_B]);C+=1
	@transaction.atomic
	def update_kategori_model(self,site_group):
		A=self;A.info('\nUpdate Kategori Model ...')
		with open(os.path.join(A.site_list,site_group,'kategori.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Kategori] at {0:.2%} '.format(G);A.info(H);I,J=kategori.objects.update_or_create(id=D[_A][_C],defaults=D[_B]);C+=1
	@transaction.atomic
	def update_tags_model(self,site_group):
		A=self;A.info('\nUpdate Tags Model ...')
		with open(os.path.join(A.site_list,site_group,'tags.json'),_D)as E:B=json.load(E)
		C=1;F=len(B)
		for D in B:G=C/F;H='\rWriting Progress [Tags] at {0:.2%} '.format(G);A.info(H);I,J=tags.objects.update_or_create(id=D[_A][_C],defaults=D[_B]);C+=1
	@transaction.atomic
	def update_menu_model(self,site_group):
		A=self;A.info('\nUpdate Menu Model ...')
		with open(os.path.join(A.site_list,site_group,'menu.json'),_D)as F:D=json.load(F)
		E=1;G=len(D)
		for B in D:
			H=E/G;I='\rWriting Progress [Menu] at {0:.2%} '.format(H);A.info(I);C,L=menu.objects.update_or_create(id=B[_A][_C],defaults=B[_B]);C.site.clear()
			for J in B[_E][_F]:K=Site.objects.get(id=J);C.site.add(K)
			C.save();E+=1
	@transaction.atomic
	def update_data_by_site(self,site_group):
		h='photo_id';g='menu_id';f='admin';e='photo';d='tags';U=site_group;R='created_at';Q=True;P=False;H=self;G='nama_seo';F='slug';E='judul_seo';H.info('\nUpdate Data By Site ...');V=os.path.join(H.site_list,U);S=[A for A in os.listdir(V)if os.path.isfile(os.path.join(V,A))]
		for K in H.model_list:
			H.info('\nproses model: '+K+'\n')
			for I in range(len(S)):
				L=S[I].split('_');M=L[len(L)-1];M=M.split('.')[:1];M=M[0];L.pop(len(L)-1);W=0;i='_'.join(L)
				if K==i:
					t=None
					with open(os.path.join(H.site_list,U,S[I]),_D)as j:X=json.load(j)
					Y=1;k=len(X)
					for A in X:
						C=apps.get_model('opd',K)
						if C:
							O=0;N=[]
							for J in C._meta.fields:N.append(J.name)
							if _F in N:O=1
							if O==0:
								N=[]
								for J in C._meta.get_fields():N.append(J.name)
								if _F in N:O=2
							Z=P;a=P;b=P;c=P
							for J in C._meta.get_fields():
								if J.name==E:c=Q
								if J.many_to_many:
									if J.name==d:Z=Q
									elif J.name==e:a=Q
									elif J.name==f:b=Q
							if K==_H:
								l=menu.objects.filter(id=A[_B][g])
								if not l:W+=1;H.info('\nSKIP',A[_B][g]);continue
							if K==_G:A[_B].pop('parent_id',None)
							m=Y/k;n='\rWriting Progress [Data Site ID '+str(M)+'] at {0:.2%} '.format(m);H.info(n)
							if h in A[_B]:
								T=photo.objects.filter(id=A[_B][h])
								if T:
									if F in A[_A]:
										B=C.objects.filter(slug=A[_A][F])
										if B:B,D=C.objects.update_or_create(slug=A[_A][F],defaults=A[_B])
										else:B=C.objects.filter(id=A[_B][_C])
										if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(slug=A[_A][F],defaults=A[_B])
										else:B=B.get()
									elif E in A[_A]:
										B=C.objects.filter(judul_seo=A[_A][E])
										if B:B,D=C.objects.update_or_create(judul_seo=A[_A][E],defaults=A[_B])
										else:
											B=C.objects.filter(id=A[_B][_C])
											if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(judul_seo=A[_A][E],defaults=A[_B])
											else:B=B.get()
									elif G in A[_A]:
										B=C.objects.filter(nama_seo=A[_A][G])
										if B:B,D=C.objects.update_or_create(nama_seo=A[_A][G],defaults=A[_B])
										else:
											B=C.objects.filter(id=A[_B][_C])
											if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(nama_seo=A[_A][G],defaults=A[_B])
											else:B=B.get()
									else:B,D=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
							elif F in A[_A]:
								B=C.objects.filter(slug=A[_A][F])
								if B:B,D=C.objects.update_or_create(slug=A[_A][F],defaults=A[_B])
								else:
									B=C.objects.filter(id=A[_B][_C])
									if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(slug=A[_A][F],defaults=A[_B])
									else:B=B.get()
							elif E in A[_A]:
								B=C.objects.filter(judul_seo=A[_A][E])
								if B:B,D=C.objects.update_or_create(judul_seo=A[_A][E],defaults=A[_B])
								else:
									B=C.objects.filter(id=A[_B][_C])
									if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(judul_seo=A[_A][E],defaults=A[_B])
									else:B=B.get()
							elif G in A[_A]:
								B=C.objects.filter(nama_seo=A[_A][G])
								if B:B,D=C.objects.update_or_create(nama_seo=A[_A][G],defaults=A[_B])
								else:
									B=C.objects.filter(id=A[_B][_C])
									if not B:A[_B].pop(_C);B,D=C.objects.update_or_create(nama_seo=A[_A][G],defaults=A[_B])
									else:B=B.get()
							else:B,D=C.objects.update_or_create(id=A[_A][_C],defaults=A[_B])
							if Z:
								B.tags.clear()
								for I in A[_E][d]:o=tags.objects.get(id=I);B.tags.add(o)
								B.save()
							if a:
								B.photo.clear()
								for I in A[_E][e]:
									T=photo.objects.filter(id=I)
									if T:p=photo.objects.get(id=I);B.photo.add(p)
								B.save()
							if b:
								B.admin.clear()
								for I in A[_E][f]:q=User.objects.get(id=I);B.admin.add(q)
								B.save()
							if O==2:
								if _E in A:
									if _F in A[_E]:
										B.site.clear()
										for r in A[_E][_F]:s=Site.objects.get(id=r);B.site.add(s)
										B.save()
							if c:
								if F in A[_A]:C.objects.filter(slug=A[_A][F]).update(slug=A[_A][F],created_at=A[_B][R])
								elif E in A[_A]:C.objects.filter(judul_seo=A[_A][E]).update(judul_seo=A[_A][E],created_at=A[_B][R])
								elif G in A[_A]:C.objects.filter(nama_seo=A[_A][G]).update(nama_seo=A[_A][G],created_at=A[_B][R])
								else:C.objects.filter(id=A[_A][_C]).update(created_at=A[_B][R])
							Y+=1
					H.info('\n')
			H.info('\nSKIP '+str(W))
	def handle(A,*F,**C):
		A.info('Begin get site data\n');B=C[_I];D=input('Confirm DB Name: ');E=settings.DATABASES
		if D==E['default']['NAME']:A.update_site_model(B);A.update_user_model(B);A.update_kategori_model(B);A.update_tags_model(B);A.update_menu_model(B);A.update_photo_model(B);A.update_data_by_site(B)
		else:A.info('\ndb_name NOT MATCH:')
		A.info('\nEnd get site data\n')