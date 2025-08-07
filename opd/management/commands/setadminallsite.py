from opd.tasks import auto_get_widget_
from django.core.management.base import BaseCommand
from opd.models import User,Site,instansi
class Command(BaseCommand):
	help='Add User Admin to All Sites'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(B,*H,**I):
		B.info('Begin Add admin');C=User.objects.get(id=1);F=Site.objects.all()
		for D in F:
			A=instansi.objects.filter(site=D)[:1]
			if A:
				A=A.get()
				for G in A.admin.all():
					E=False
					if G.id==C.id:E=True;break
				if not E:A.admin.add(C);B.info('Add '+C.username+' to '+D.domain)
		B.info('End Add admin')