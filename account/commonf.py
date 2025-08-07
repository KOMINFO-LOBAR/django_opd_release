from django.db.models import Subquery
from opd.models import photo
def get_topFoto(model_criteria):return Subquery(photo.objects.filter(**model_criteria).order_by('jenis').values('file_path')[:1])