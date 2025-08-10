from django.core.management.base import BaseCommand
from opd.models import Log
class Command(BaseCommand):
	help='Scan template and menu default for reference create dashboard menu'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def clear_log(A):B=Log.objects.all().delete();A.info('All Done ...')
	def handle(A,*B,**C):A.clear_log()