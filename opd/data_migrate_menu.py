_E='is_initial_data'
_D='is_visibled'
_C='order_menu'
_B='parent_id'
_A=None
from django.db import transaction
from opd.models import instansi,menu
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from menu.models import MenuGroup,Menu,OptMenuKinds
def recursive_parent_menu(site_id,parent_id,m_menu_group):
	E=m_menu_group;D=parent_id;C=site_id;A=Menu.objects.get(id=D)
	if A.parent:F=str(C)+str(A.parent.id);recursive_parent_menu(C,A.parent.id,E)
	else:F=_A
	if A.is_admin_menu:G=OptMenuKinds.BACKEND
	else:G=OptMenuKinds.FRONTEND
	B,H=Menu.objects.language('id').get_or_create(id=str(C)+str(A.id),defaults={'name':A.name,_B:F,'link':A.href,_C:A.order_menu,'icon':A.icon,'kind':G,_D:A.is_visibled,_E:A.is_master_menu})
	if H:B.menu_group.add(E);B.set_current_language('en');B.name=A.name;B.save()
@transaction.atomic
def migrate_menu():
	C=0;N=Site.objects.all()
	for I in N:
		C=I.id;J=I.domain.replace(':','.');B='';E=instansi.objects.filter(site_id=C)[:1]
		if E:E=E[0];B=E.nama
		if B:B=B.replace(' ','')[:10];B=B.lower()
		F=_A
		if B:F,G=Group.objects.get_or_create(name=B+'.'+J)
		H=_A;
		if F:H,G=MenuGroup.objects.get_or_create(site_id=C,group=F)
		if H:
			K=menu.objects.order_by(_B,_C);
			for A in K:
				if A.is_admin_menu:L=OptMenuKinds.BACKEND
				else:L=OptMenuKinds.FRONTEND
				if A.parent:M=str(C)+str(A.parent.id);recursive_parent_menu(C,A.parent.id,H)
				else:M=_A
				D,G=Menu.objects.language('id').get_or_create(id=str(C)+str(A.id),defaults={'name':A.name,_B:M,'link':A.href,_C:A.order_menu,'icon':A.icon,'kind':L,_D:A.is_visibled,_E:A.is_master_menu})
				if G:D.menu_group.add(H);D.set_current_language('en');D.name=A.name;D.save()
	return True