from opd.tasks import auto_get_widget_
from django.core.management.base import BaseCommand
from opd.models import User,Site,instansi
class Command(BaseCommand):
	help='Add User Admin to All Sites'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(C,*H,**I):
		C.info('Begin Add admin');B=User.objects.get(id=1);G=Site.objects.all()
		for D in G:
			A=instansi.objects.filter(site=D);print(A)
			if A:
				A=A.get()
				for E in A.admin.all():
					F=False;print(E.id,B.id)
					if E.id==B.id:F=True;break
				if not F:A.admin.add(B);C.info('Add '+B.username+' to '+D.domain)
		C.info('End Add admin')