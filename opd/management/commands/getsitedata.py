_A='site'
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_A);photo_dir=os.path.join(base_dir,'media','images');model_list=['photo','kategori','tags','berita','comment','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','menu','pejabat','halaman_statis','agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def get_data(K,site_id,sub_folder):
		E=site_id
		for F in K.model_list:
			print('proses model: ',F);B=apps.get_model('opd',F);A=0;C=[]
			for G in B._meta.fields:C.append(G.name)
			if _A in C:A=1
			if A==0:
				C=[]
				for G in B._meta.get_fields():C.append(G.name)
				if _A in C:A=2
			H=[];D=None
			if A==1:D=B.objects.filter(site_id=E)
			elif A==2:D=B.objects.filter(site__id=E)
			elif A==0:D=B.objects.all()
			if D:
				L=list(D.values());O=len(L)
				for P in range(O):
					M={}
					for (I,N) in L[P].items():
						if I=='id':Q={I:N}
						else:M[I]=N
					H.append({'condition':Q,'defaults':M})
				if H:
					J=os.path.join(K.site_list,sub_folder)
					if not os.path.exists(J):os.makedirs(J)
					R=os.path.join(J,f"{F}_{E}.json")
					with open(R,'w')as S:S.write(json.dumps(H,cls=DjangoJSONEncoder))
				else:print('empty table')
			else:print('---EMPTY TABLE---',A)
	def get_data_by_site(A):
		print('Get Site Data ...');B=[B for B in os.listdir(A.site_list)if os.path.isfile(os.path.join(A.site_list,B))];A.info('list_file: ['+', '.join(B)+']');E=[A.split('_')[len(A.split('_'))-1]for A in B];A.info('res_folder: ['+', '.join(E)+']')
		for D in range(len(B)):
			A.info('proses: '+B[D])
			with open(os.path.join(A.site_list,B[D]),'r')as G:C=G.read()
			C=C.split('\n')
			for F in range(len(C)):
				if C[F]:A.get_data(C[F],E[D])
	def handle(A,*B,**C):A.info('Begin get site data');A.get_data_by_site();A.info('End get site data')