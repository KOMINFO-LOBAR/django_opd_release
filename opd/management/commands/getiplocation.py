from opd.tasks import geo_location_hitcount
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Update data with real IP Location'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin get IP location');geo_location_hitcount(max_data=100);A.info('End get IP Location')