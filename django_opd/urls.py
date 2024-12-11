from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include,path
from account.forms import UserLoginForm
from django.contrib.auth import views
urlpatterns=[path('',include('opd.urls')),path('',include('account.urls')),path('captcha/login/',views.LoginView.as_view(template_name='registration/login.html',authentication_form=UserLoginForm),name='login'),path('secret-admin/',admin.site.urls),path('__debug__/',include('debug_toolbar.urls')),path('ckeditor5/',include('django_ckeditor_5.urls'),name='ck_editor_5_upload_file')]
if settings.DEBUG:urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT);urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
else:urlpatterns+=staticfiles_urlpatterns()