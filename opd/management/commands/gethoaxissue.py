from opd.tasks import auto_get_hoax_issue_
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Get Hoax Issue'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin get Hoax Issue');auto_get_hoax_issue_();A.info('End get Hoax Issue')