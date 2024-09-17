_M='order_menu'
_L='parent_id'
_K='site'
_J='empty table'
_I='w'
_H='defaults'
_G='condition'
_F=True
_E=False
_D='id'
_C='nama_seo'
_B='slug'
_A='judul_seo'
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
	help='Detach all table base on site id';base_dir=settings.BASE_DIR;site_list=os.path.join(base_dir,_K);photo_dir=os.path.join(base_dir,'media','images');model_list=['berita','pengumuman','artikel','dokumen','link_terkait','galery_foto','galery_layanan','galery_video','instansi_kategori','instansi','social_media','logo','banner','pejabat','halaman_statis','agenda','popup','info_hoax','info_widget','banner_all']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def get_site_model(M,sub_folder):
		L='Site.json';D=os.path.join(M.site_list,sub_folder);E=os.path.join(D,L)
		if not os.path.isfile(E):
			H=Site.objects.all()
			if H:
				I=list(H.values());N=len(I);F=[]
				for O in range(N):
					G={};B=I[O].items();J=_E
					if _A in B or _B in B or _C in B:J=_F
					if not J:
						for(A,C)in B:
							if A==_D:K={A:C}
							else:G[A]=C
					else:
						for(A,C)in B:
							if A==_A or A==_B or A==_C:K={A:C}
							else:G[A]=C
					F.append({_G:K,_H:G})
				if F:
					if not os.path.exists(D):os.makedirs(D)
					E=os.path.join(D,L)
					with open(E,_I)as P:P.write(json.dumps(F,cls=DjangoJSONEncoder))
				else:pass
	def get_user_model(M,sub_folder):
		L='User.json';D=os.path.join(M.site_list,sub_folder);E=os.path.join(D,L)
		if not os.path.isfile(E):
			H=User.objects.all()
			if H:
				I=list(H.values());N=len(I);F=[]
				for O in range(N):
					G={};B=I[O].items();J=_E
					if _A in B or _B in B or _C in B:J=_F
					if not J:
						for(A,C)in B:
							if A==_D:K={A:C}
							else:G[A]=C
					else:
						for(A,C)in B:
							if A==_A or A==_B or A==_C:K={A:C}
							else:G[A]=C
					F.append({_G:K,_H:G})
				if F:
					if not os.path.exists(D):os.makedirs(D)
					E=os.path.join(D,L)
					with open(E,_I)as P:P.write(json.dumps(F,cls=DjangoJSONEncoder))
				else:pass
	def get_photo_model(M,sub_folder):
		L='photo.json';D=os.path.join(M.site_list,sub_folder);E=os.path.join(D,L)
		if not os.path.isfile(E):
			H=photo.objects.all()
			if H:
				I=list(H.values());N=len(I);F=[]
				for O in range(N):
					G={};B=I[O].items();J=_E
					if _A in B or _B in B or _C in B:J=_F
					if not J:
						for(A,C)in B:
							if A==_D:K={A:C}
							else:G[A]=C
					else:
						for(A,C)in B:
							if A==_A or A==_B or A==_C:K={A:C}
							else:G[A]=C
					F.append({_G:K,_H:G})
				if F:
					if not os.path.exists(D):os.makedirs(D)
					E=os.path.join(D,L)
					with open(E,_I)as P:P.write(json.dumps(F,cls=DjangoJSONEncoder))
				else:pass
	def get_kategori_model(M,sub_folder):
		L='kategori.json';D=os.path.join(M.site_list,sub_folder);E=os.path.join(D,L)
		if not os.path.isfile(E):
			H=kategori.objects.all()
			if H:
				I=list(H.values());N=len(I);F=[]
				for O in range(N):
					G={};B=I[O].items();J=_E
					if _A in B or _B in B or _C in B:J=_F
					if not J:
						for(A,C)in B:
							if A==_D:K={A:C}
							else:G[A]=C
					else:
						for(A,C)in B:
							if A==_A or A==_B or A==_C:K={A:C}
							else:G[A]=C
					F.append({_G:K,_H:G})
				if F:
					if not os.path.exists(D):os.makedirs(D)
					E=os.path.join(D,L)
					with open(E,_I)as P:P.write(json.dumps(F,cls=DjangoJSONEncoder))
				else:pass
	def get_tags_model(M,sub_folder):
		L='tags.json';D=os.path.join(M.site_list,sub_folder);E=os.path.join(D,L)
		if not os.path.isfile(E):
			H=tags.objects.all()
			if H:
				I=list(H.values());N=len(I);F=[]
				for O in range(N):
					G={};B=I[O].items();J=_E
					if _A in B or _B in B or _C in B:J=_F
					if not J:
						for(A,C)in B:
							if A==_D:K={A:C}
							else:G[A]=C
					else:
						for(A,C)in B:
							if A==_A or A==_B or A==_C:K={A:C}
							else:G[A]=C
					F.append({_G:K,_H:G})
				if F:
					if not os.path.exists(D):os.makedirs(D)
					E=os.path.join(D,L)
					with open(E,_I)as P:P.write(json.dumps(F,cls=DjangoJSONEncoder))
				else:pass
	def is_have_child(D,menu_id):
		B=menu.objects.filter(parent_id=menu_id).order_by(_L,_M).values(_D);A=[]
		for C in B:A.append(C[_D])
		return A
	def create_menu_recursive(C,root_menu_id,mList_recursive):
		A=mList_recursive
		for B in root_menu_id:
			D=C.is_have_child(B)
			if D:A.append({_D:B});C.create_menu_recursive(D,A)
			else:A.append({_D:B})
	def get_menu_model(F,sub_folder):
		N='menu.json';B=os.path.join(F.site_list,sub_folder);D=os.path.join(B,N);O=menu.objects.filter(parent=None).order_by(_L,_M).values(_D);G=[]
		for P in O:G.append(P[_D])
		H=[];F.create_menu_recursive(G,H)
		if not os.path.isfile(D):
			E=[]
			for C in H:
				I=menu.objects.filter(id=C[_D])
				if I:
					J=list(I.values());Q=len(J)
					for R in range(Q):
						K={}
						for(A,C)in J[R].items():
							if A==_D:L={A:C}
							else:K[A]=C
						M=[]
						for A in menu.objects.get(id=L[_D]).site.all():M.append(A.id)
						S={_K:M};E.append({_G:L,_H:K,'m2m':S})
					if E:
						if not os.path.exists(B):os.makedirs(B)
						D=os.path.join(B,N)
						with open(D,_I)as T:T.write(json.dumps(E,cls=DjangoJSONEncoder))
					else:pass
		else:pass
	def get_data(T,site_id,sub_folder):
		c='admin';b='photo';a='tags';M=site_id
		for N in T.model_list:
			D=apps.get_model('opd',N);F=0;I=[]
			for G in D._meta.fields:I.append(G.name)
			if _K in I:F=1
			if F==0:
				I=[]
				for G in D._meta.get_fields():I.append(G.name)
				if _K in I:F=2
			U=_E;V=_E;W=_E
			for G in D._meta.get_fields():
				if G.many_to_many:
					if G.name==a:U=_F
					elif G.name==b:V=_F
					elif G.name==c:W=_F
			K=[];J=None
			if F==1:J=D.objects.filter(site_id=M)
			elif F==2:J=D.objects.filter(site__id=M)
			elif F==0:J=D.objects.all()
			if J:
				X=list(J.values());d=len(X)
				for e in range(d):
					L={};O=X[e].items();Y=_E;f=[_A,_B,_C]
					for(A,H)in O:
						if A in f:Y=_F;break
					if not Y:
						for(A,H)in O:
							if A==_D:B={A:H}
							else:L[A]=H
					else:
						for(A,H)in O:
							if A==_A or A==_B or A==_C:B={A:H}
							else:L[A]=H
					Z={}
					if U:
						C=[];
						if _B in B:
							for A in D.objects.get(slug=B[_B]).tags.all():C.append(A.id)
						elif _A in B:
							for A in D.objects.get(judul_seo=B[_A]).tags.all():C.append(A.id)
						elif _C in B:
							for A in D.objects.get(nama_seo=B[_C]).tags.all():C.append(A.id)
						else:
							for A in D.objects.get(id=B[_D]).tags.all():C.append(A.id)
						Z={a:C}
					P={}
					if V:
						C=[]
						if _B in B:
							for A in D.objects.get(slug=B[_B]).photo.all():C.append(A.id)
						elif _A in B:
							for A in D.objects.get(judul_seo=B[_A]).photo.all():C.append(A.id)
						elif _C in B:
							for A in D.objects.get(nama_seo=B[_C]).photo.all():C.append(A.id)
						else:
							for A in D.objects.get(id=B[_D]).photo.all():C.append(A.id)
						P={b:C}
					Q={}
					if W:
						C=[]
						if _B in B:
							for A in D.objects.get(slug=B[_B]).admin.all():C.append(A.id)
						elif _A in B:
							for A in D.objects.get(judul_seo=B[_A]).admin.all():C.append(A.id)
						elif _C in B:
							for A in D.objects.get(nama_seo=B[_C]).admin.all():C.append(A.id)
						else:
							for A in D.objects.get(id=B[_D]).admin.all():C.append(A.id)
						Q={c:C}
					R={}
					if F==2:
						C=[]
						if _B in B:
							for A in D.objects.get(slug=B[_B]).site.all():C.append(A.id)
						elif _A in B:
							for A in D.objects.get(judul_seo=B[_A]).site.all():C.append(A.id)
						elif _C in B:
							for A in D.objects.get(nama_seo=B[_C]).site.all():C.append(A.id)
						else:
							for A in D.objects.get(id=B[_D]).site.all():C.append(A.id)
						R={_K:C}
					E=Z
					if E:E.update(P)
					else:E=P
					if E:E.update(Q)
					else:E=Q
					if E:E.update(R)
					else:E=R
					if E:K.append({_G:B,_H:L,'m2m':E})
					else:K.append({_G:B,_H:L})
				if K:
					S=os.path.join(T.site_list,sub_folder)
					if not os.path.exists(S):os.makedirs(S)
					g=os.path.join(S,f"{N}_{M}.json")
					with open(g,_I)as h:h.write(json.dumps(K,cls=DjangoJSONEncoder))
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