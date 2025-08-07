from opd.data_weather import get_data_weather
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Get Weather Info'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):A.info('Begin get Weather Info');get_data_weather();A.info('End get Weather Info')