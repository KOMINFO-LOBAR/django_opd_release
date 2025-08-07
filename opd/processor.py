from functools import lru_cache
from django.conf import settings
from django.contrib.sites.models import Site
from opd.models import comment
from opd.views import get_siteID
@lru_cache(2)
def my_context(request):A=settings.DEBUG;return{'debug_flag':A}
@lru_cache(100)
def my_comment_count(request):A=get_siteID(request);B=comment.objects.filter(site_id=A,active=False).count();return{'comment_count':B}
def get_static_version(request):A=settings.STATIC_VERSION;return{'static_version':A}
def site_id(request):
	B='site_id';A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=True)
	if A:return{B:A[0]}
	return{B:0}