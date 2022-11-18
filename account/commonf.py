from datetime import datetime,timedelta
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.db.models import Count,OuterRef,Subquery
from opd.models import photo
def get_topFoto(model_criteria):return Subquery(photo.objects.filter(**model_criteria).order_by('jenis').values('file_path')[:1])