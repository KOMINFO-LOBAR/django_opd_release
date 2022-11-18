from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views
urlpatterns=[path('',include('opd.urls')),path('',include('account.urls')),path('secret-admin/',admin.site.urls),path('ckeditor/',include('ckeditor_uploader.urls')),path('ckeditor/upload/',login_required(ckeditor_views.upload),name='ckeditor_upload'),path('ckeditor/browse/',never_cache(login_required(ckeditor_views.browse)),name='ckeditor_browse')]
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:urlpatterns+=staticfiles_urlpatterns()