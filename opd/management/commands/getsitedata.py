_H='order_menu'
_G='parent_id'
_F='site'
_E='empty table'
_D='w'
_C='defaults'
_B='condition'
_A='id'
import os
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings
from django.apps import apps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from opd.models import kategori,tags,menu,photo
class Command(BaseCommand):
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_F);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','pejabat','halaman_statis','agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def get_site_model(J,sub_folder):
		I='Site.json';print('Proses SITE ID');A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=Site.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for (D,H) in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:print(_E)
	def get_user_model(J,sub_folder):
		I='User.json';print('Proses USER MODEL');A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=User.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for (D,H) in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:print(_E)
	def get_photo_model(J,sub_folder):
		I='photo.json';print('Proses PHOTO MODEL');A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=photo.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for (D,H) in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:print(_E)
	def get_kategori_model(J,sub_folder):
		I='kategori.json';print('Proses KATEGORI MODEL');A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=kategori.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for (D,H) in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:print(_E)
	def get_tags_model(J,sub_folder):
		I='tags.json';print('Proses TAGS MODEL');A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=tags.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for (D,H) in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:print(_E)
	def is_have_child(D,menu_id):
		B=menu.objects.filter(parent_id=menu_id).order_by(_G,_H).values(_A);A=[]
		for C in B:A.append(C[_A])
		return A
	def create_menu_recursive(C,root_menu_id,mList_recursive):
		A=mList_recursive
		for B in root_menu_id:
			D=C.is_have_child(B)
			if D:A.append({_A:B});C.create_menu_recursive(D,A)
			else:A.append({_A:B})
	def get_menu_model(F,sub_folder):
		L='menu.json';print('Proses MENU MODEL');A=os.path.join(F.site_list,sub_folder);C=os.path.join(A,L);M=menu.objects.filter(parent=None).order_by(_G,_H).values(_A);G=[]
		for N in M:G.append(N[_A])
		H=[];F.create_menu_recursive(G,H)
		if not os.path.isfile(C):
			print('Recreate menu');D=[]
			for B in H:
				I=menu.objects.filter(id=B[_A])
				if I:
					J=list(I.values());O=len(J)
					for P in range(O):
						K={}
						for (E,B) in J[P].items():
							if E==_A:Q={E:B}
							else:K[E]=B
						D.append({_B:Q,_C:K})
					if D:
						if not os.path.exists(A):os.makedirs(A)
						C=os.path.join(A,L)
						with open(C,_D)as R:R.write(json.dumps(D,cls=DjangoJSONEncoder))
					else:print(_E)
		else:print('menu not recreate')
	def get_data(Q,site_id,sub_folder):
		b='admin';a='photo';Z='tags';P=True;O=False;K=site_id
		for L in Q.model_list:
			print('proses model: ',L);A=apps.get_model('opd',L);E=0;F=[]
			for C in A._meta.fields:F.append(C.name)
			if _F in F:E=1
			if E==0:
				F=[]
				for C in A._meta.get_fields():F.append(C.name)
				if _F in F:E=2
			R=O;S=O;T=O
			for C in A._meta.get_fields():
				if C.many_to_many:
					if C.name==Z:R=P
					elif C.name==a:S=P
					elif C.name==b:T=P
			I=[];G=None
			if E==1:G=A.objects.filter(site_id=K)
			elif E==2:G=A.objects.filter(site__id=K)
			elif E==0:G=A.objects.all()
			if G:
				U=list(G.values());c=len(U)
				for d in range(c):
					M={}
					for (B,V) in U[d].items():
						if B==_A:H={B:V}
						else:M[B]=V
					W={}
					if R:
						D=[]
						for B in A.objects.get(id=H[_A]).tags.all():D.append(B.id)
						W={Z:D}
					X={}
					if S:
						D=[]
						for B in A.objects.get(id=H[_A]).photo.all():D.append(B.id)
						X={a:D}
					Y={}
					if T:
						D=[]
						for B in A.objects.get(id=H[_A]).admin.all():D.append(B.id)
						Y={b:D}
					J=W;J.update(X);J.update(Y)
					if J:I.append({_B:H,_C:M,'m2m':J})
					else:I.append({_B:H,_C:M})
				if I:
					N=os.path.join(Q.site_list,sub_folder)
					if not os.path.exists(N):os.makedirs(N)
					e=os.path.join(N,f"{L}_{K}.json")
					with open(e,_D)as f:f.write(json.dumps(I,cls=DjangoJSONEncoder))
				else:print(_E)
			else:print('---EMPTY TABLE---',E)
	def get_data_by_site(A):
		D=[B for B in os.listdir(A.site_list)if os.path.isfile(os.path.join(A.site_list,B))];A.info('list_file: ['+', '.join(D)+']');B=[A.split('_')[len(A.split('_'))-1]for A in D]
		for F in range(len(B)):B[F]=B[F].split('.')[0]
		A.info('res_folder: ['+', '.join(B)+']')
		for C in range(len(D)):
			A.info('proses: '+D[C])
			with open(os.path.join(A.site_list,D[C]),'r')as H:E=H.read()
			E=E.split('\n')
			for G in range(len(E)):
				if E[G]:A.get_site_model(B[C]);A.get_user_model(B[C]);A.get_kategori_model(B[C]);A.get_tags_model(B[C]);A.get_menu_model(B[C]);A.get_photo_model(B[C]);A.get_data(E[G],B[C])
	def handle(A,*D,**E):
		A.info('Begin get site data');B=input('Confirm DB Name: ');C=settings.DATABASES
		if B==C['default']['NAME']:A.get_data_by_site()
		else:print('db_name NOT MATCH:')
		A.info('End get site data')