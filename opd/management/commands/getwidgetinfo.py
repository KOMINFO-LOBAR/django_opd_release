from opd.tasks import auto_get_widget_
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Get Widget Info'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin get Widget Info');auto_get_widget_();A.info('End get Widget Info')