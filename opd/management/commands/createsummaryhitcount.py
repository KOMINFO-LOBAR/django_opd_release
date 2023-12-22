from opd.tasks import summary_hitcount
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Create Summary Hitcount'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin summary hitcount');summary_hitcount(1);A.info('End summary hitcount')