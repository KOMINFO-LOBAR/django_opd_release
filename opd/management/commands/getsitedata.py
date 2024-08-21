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
		I='Site.json';A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=Site.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for(D,H)in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:pass
	def get_user_model(J,sub_folder):
		I='User.json';A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=User.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for(D,H)in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:pass
	def get_photo_model(J,sub_folder):
		I='photo.json';A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=photo.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for(D,H)in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:pass
	def get_kategori_model(J,sub_folder):
		I='kategori.json';A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=kategori.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for(D,H)in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:pass
	def get_tags_model(J,sub_folder):
		I='tags.json';A=os.path.join(J.site_list,sub_folder);B=os.path.join(A,I)
		if not os.path.isfile(B):
			E=tags.objects.all()
			if E:
				F=list(E.values());K=len(F);C=[]
				for L in range(K):
					G={}
					for(D,H)in F[L].items():
						if D==_A:M={D:H}
						else:G[D]=H
					C.append({_B:M,_C:G})
				if C:
					if not os.path.exists(A):os.makedirs(A)
					B=os.path.join(A,I)
					with open(B,_D)as N:N.write(json.dumps(C,cls=DjangoJSONEncoder))
				else:pass
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
		N='menu.json';B=os.path.join(F.site_list,sub_folder);D=os.path.join(B,N);O=menu.objects.filter(parent=None).order_by(_G,_H).values(_A);G=[]
		for P in O:G.append(P[_A])
		H=[];F.create_menu_recursive(G,H)
		if not os.path.isfile(D):
			E=[]
			for C in H:
				I=menu.objects.filter(id=C[_A])
				if I:
					J=list(I.values());Q=len(J)
					for R in range(Q):
						K={}
						for(A,C)in J[R].items():
							if A==_A:L={A:C}
							else:K[A]=C
						M=[]
						for A in menu.objects.get(id=L[_A]).site.all():M.append(A.id)
						S={_F:M};E.append({_B:L,_C:K,'m2m':S})
					if E:
						if not os.path.exists(B):os.makedirs(B)
						D=os.path.join(B,N)
						with open(D,_D)as T:T.write(json.dumps(E,cls=DjangoJSONEncoder))
					else:pass
		else:pass
	def get_data(T,site_id,sub_folder):
		c='admin';b='photo';a='tags';S=True;R=False;K=site_id
		for L in T.model_list:
			D=apps.get_model('opd',L);E=0;H=[]
			for F in D._meta.fields:H.append(F.name)
			if _F in H:E=1
			if E==0:
				H=[]
				for F in D._meta.get_fields():H.append(F.name)
				if _F in H:E=2
			U=R;V=R;W=R
			for F in D._meta.get_fields():
				if F.many_to_many:
					if F.name==a:U=S
					elif F.name==b:V=S
					elif F.name==c:W=S
			J=[];I=None
			if E==1:I=D.objects.filter(site_id=K)
			elif E==2:I=D.objects.filter(site__id=K)
			elif E==0:I=D.objects.all()
			if I:
				X=list(I.values());d=len(X)
				for e in range(d):
					M={}
					for(A,Y)in X[e].items():
						if A==_A:G={A:Y}
						else:M[A]=Y
					Z={}
					if U:
						B=[]
						for A in D.objects.get(id=G[_A]).tags.all():B.append(A.id)
						Z={a:B}
					N={}
					if V:
						B=[]
						for A in D.objects.get(id=G[_A]).photo.all():B.append(A.id)
						N={b:B}
					O={}
					if W:
						B=[]
						for A in D.objects.get(id=G[_A]).admin.all():B.append(A.id)
						O={c:B}
					P={}
					if E==2:
						B=[]
						for A in D.objects.get(id=G[_A]).site.all():B.append(A.id)
						P={_F:B}
					C=Z
					if C:C.update(N)
					else:C=N
					if C:C.update(O)
					else:C=O
					if C:C.update(P)
					else:C=P
					if C:J.append({_B:G,_C:M,'m2m':C})
					else:J.append({_B:G,_C:M})
				if J:
					Q=os.path.join(T.site_list,sub_folder)
					if not os.path.exists(Q):os.makedirs(Q)
					f=os.path.join(Q,f"{L}_{K}.json")
					with open(f,_D)as g:g.write(json.dumps(J,cls=DjangoJSONEncoder))
				else:pass
			else:pass
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
		else:pass
		A.info('End get site data')