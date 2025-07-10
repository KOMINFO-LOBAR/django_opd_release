from .models import halaman_statis
from django.db import transaction
@transaction.atomic
def clean_unused_pages():
	A=halaman_statis.objects.filter(isi_halaman__icontains='informasi tentang').filter(isi_halaman__icontains='silahkan update').filter(isi_halaman__icontains='dashboard');B=A.count()
	if B>0:A.delete();return True
	return False