_G='activeMenu'
_F=' - '
_E=None
_D='href'
_C='parent_id'
_B='id'
_A='nama'
from .models import menu
from django.db.models import F
import logging
logger=logging.getLogger(__name__)
class ClsMenus:
	mDict={};mList=[]
	def __init__(A,key_filter=0,pIs_admin_menu=False,pIs_master_menu=False):
		D=pIs_master_menu;C=pIs_admin_menu;B=key_filter
		if B>0:
			if len(A.mList)==0:A.create_menus(B,C,D)
			else:A.mDict={};A.mList=[];A.create_menus(B,C,D)
	def get_menus(A):return A.mList
	def convert_StrToList(B,str):A=list(str.split(_F));return A
	def find_activeMenuList(B,act_menu):
		A=0;C=[]
		while A<len(B.mList):
			if act_menu.lower()==B.mList[A][_A].lower():C=B.mList[A][_G];break
			A+=1
		return C
	def get_menuLevel(D,key_filter,menu_id):
		B=key_filter;id=menu_id;C=0;A=menu.objects.filter(site__id=B,id=id).first()
		if A:
			while A.parent_id is not _E:
				C+=1;id=A.parent_id;A=menu.objects.filter(site__id=B,id=id).first()
				if not A:break
		return C
	def create_breadCrumb(C,act_menu):
		H=act_menu;D={};F=[];A=0;B=0;G=0;E=''
		if len(C.mList)>0:
			E=C.mList[0][_A]
			if E.lower()!=H.lower():D[A]={_B:A,_A:E,_D:C.mList[0][_D]}
			else:D[A]={_B:A,_A:E,_D:'#'}
			F.append(D[A]);A+=1;I=1
		if E.lower()!=H.lower():
			while B<len(C.mList):
				E=C.mList[B][_A]
				if E.lower()==H.lower():G=C.mList[B][_C];D[A]={_B:A,_A:C.mList[B][_A],_D:'#'};F.append(D[A]);A+=1;break
				B+=1
			B=0
			while B<len(C.mList):
				if G is _E:break
				elif G==C.mList[B][_B]:G=C.mList[B][_C];D[A]={_B:A,_A:C.mList[B][_A],_D:C.mList[B][_D]};F.insert(I,D[A]);A+=1;I+=1;B=0
				B+=1
		return F
	def create_menus(A,key_filter,pIs_admin_menu,pIs_master_menu):
		R='haveChildEndTag';Q='haveChild';P='order_menu';L=pIs_admin_menu;J=key_filter;menu.objects.filter(id=F(_C)).update(parent_id=_E)
		if pIs_master_menu:M=menu.objects.filter(site__id=J,is_admin_menu=L).order_by(_C,P)
		else:M=menu.objects.filter(site__id=J,is_admin_menu=L,is_visibled=True).order_by(_C,P)
		G=''
		for E in M:G=E.id;A.mDict[G]={_B:G,_A:E.nama,_D:E.href,'icon':E.icon,_C:E.parent_id,'is_visibled':E.is_visibled};A.mList.append(A.mDict[G])
		B=0;C=0;K=0
		while B<len(A.mList):
			C=B+1;K=0
			while C<len(A.mList):
				if A.mList[B][_B]==A.mList[C][_C]:K+=1;A.mList.insert(B+K,A.mList[C]);A.mList.pop(C+1)
				C+=1
			B+=1
		B=0;H=0;N=0;I=0;S=0
		while B<len(A.mList):
			H=A.get_menuLevel(J,A.mList[B][_B]);A.mList[B]['level']=H;A.mList[B][Q]=0
			if B>0:
				if A.mList[B][_C]==A.mList[B-1][_B]:A.mList[B-1][Q]=1
			A.mList[B][R]=0;O=H-N
			if O<0:A.mList[B-1][R]=-O
			N=H;B+=1
		D='';B=0;C=0
		while B<len(A.mList):
			I=A.mList[B][_C];C=0;D=''
			while C<len(A.mList):
				if I is _E:
					if D!='':D+=_F
					D+=A.mList[B][_A];break
				elif I==A.mList[C][_B]:
					if D!='':D+=_F
					D+=A.mList[C][_A];I=A.mList[C][_C];C=0
				C+=1
			A.mList[B][_G]=A.convert_StrToList(D.lower());B+=1