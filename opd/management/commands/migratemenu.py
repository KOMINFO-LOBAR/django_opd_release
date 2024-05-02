from opd.data_migrate_menu import migrate_menu
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Run once for patch menu'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin migate menu');migrate_menu();A.info('End migate menu')