_E='is_initial_data'
_D='is_visibled'
_C='order_menu'
_B='parent_id'
_A=None
from django.db import transaction
from opd.models import menu,instansi
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from menu.models import MenuGroup,Menu,OptMenuKinds
def recursive_parent_menu(site_id,parent_id,m_menu_group):
	E=m_menu_group;D=parent_id;C=site_id;A=menu.objects.get(id=D)
	if A.parent:F=str(C)+str(A.parent.id);print('Inside recursive function',D);recursive_parent_menu(C,A.parent.id,E)
	else:F=_A
	if A.is_admin_menu:G=OptMenuKinds.BACKEND
	else:G=OptMenuKinds.FRONTEND
	B,H=Menu.objects.language('id').get_or_create(id=str(C)+str(A.id),defaults={'name':A.nama,_B:F,'link':A.href,_C:A.order_menu,'icon':A.icon,'kind':G,_D:A.is_visibled,_E:A.is_master_menu})
	if H:B.menu_group.add(E);B.set_current_language('en');B.name=A.nama;B.save()
@transaction.atomic
def migrate_menu():
	B=0;M=Site.objects.all()
	for H in M:
		print('Site: ',H.id);B=H.id;J=H.domain.replace(':','.');C='';E=instansi.objects.filter(site_id=B)[:1]
		if E:E=E[0];C=E.nama
		if C:C=C.replace(' ','')[:10];C=C.lower()
		print('Nama Instansi',C,B,J);I=_A
		if C:I,F=Group.objects.get_or_create(name=C+'.'+J)
		G=_A
		if I:G,F=MenuGroup.objects.get_or_create(site_id=B,group=I)
		if G:
			N=menu.objects.filter(site__id=B).order_by(_B,_C)
			for A in N:
				print('Data: ',str(B)+str(A.id),A.nama)
				if A.is_admin_menu:K=OptMenuKinds.BACKEND
				else:K=OptMenuKinds.FRONTEND
				if A.parent:L=str(B)+str(A.parent.id);recursive_parent_menu(B,A.parent.id,G)
				else:L=_A
				D,F=Menu.objects.language('id').get_or_create(id=str(B)+str(A.id),defaults={'name':A.nama,_B:L,'link':A.href,_C:A.order_menu,'icon':A.icon,'kind':K,_D:A.is_visibled,_E:A.is_master_menu})
				if F:D.menu_group.add(G);D.set_current_language('en');D.name=A.nama;D.save()
				print('Create menu ',D,F)
	return True