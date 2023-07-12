from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include,path
urlpatterns=[path('',include('opd.urls')),path('',include('account.urls')),path('secret-admin/',admin.site.urls),path('__debug__/',include('debug_toolbar.urls')),path('ckeditor5/',include('django_ckeditor_5.urls'),name='ck_editor_5_upload_file')]
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT);urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
else:urlpatterns+=staticfiles_urlpatterns()