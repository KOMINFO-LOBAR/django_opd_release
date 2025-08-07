from opd.tasks import session_cleanup
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Execute Clear Sessions Now'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin clear sessions');session_cleanup();A.info('End Clear Sessions')