from opd.tasks import clean_unused_pages_
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Clear Unuse pages'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin clear unuse pages');clean_unused_pages_();A.info('End Clear unuse pages')