from functools import lru_cache
from django.conf import settings
from opd.models import comment
from opd.views import get_siteID
@lru_cache(2)
def my_context(request):A=settings.DEBUG;return{'debug_flag':A}
@lru_cache(100)
def my_comment_count(request):A=get_siteID(request);B=comment.objects.filter(site_id=A,active=False).count();return{'comment_count':B}