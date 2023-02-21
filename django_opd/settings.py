_T='youtube'
_S='plain-text'
_R='extraPlugins'
_Q='pasteFilter'
_P='toolbarCanCollapse'
_O='toolbar'
_N='MEDIA_ROOT'
_M='STATIC_ROOT'
_L='DB_NAME'
_K='DB_ENGINE'
_J='ENGINE'
_I='OPTIONS'
_H='BACKEND'
_G='embed_video'
_F='ALLOWED_HOSTS'
_E='SECRET_KEY'
_D='DB_PASSWORD'
_C='NAME'
_B='default'
_A=True
import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent.parent
from encryption import OutboxEncryption
lib=OutboxEncryption(BASE_DIR)
lib.set_keyword_local('env_opd')
lib.set_keyword_local('venv')
mplaint_key=[_D,_E]
mplaint_list=[_F]
key=lib.decrypt_environ(mplaint_key,mplaint_list)
if not key:raise Exception('No data found in environment, activate environment first!')
SECRET_KEY=key[_E]
DEBUG=key['DEBUG']
UNDER_CONSTRUCTION=key['UNDER_CONSTRUCTION']
UNDER_CONSTRUCTION_TEMPLATE='opd/construction.html'
LOGIN_REDIRECT_URL='/dashboard/dashboard'
LOGOUT_REDIRECT_URL='/'
ALLOWED_HOSTS=key[_F]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','django.contrib.sites','django.contrib.humanize',_G,'simple_open_graph','django_social_share','hitcount','opd','account','django_underconstruction','import_export','ckeditor','ckeditor_uploader','corsheaders','debug_toolbar']
CKEDITOR_UPLOAD_PATH='uploads/'
CKEDITOR_BASEPATH='/static/ckeditor/ckeditor/'
EMAIL_HOST='localhost'
EMAIL_PORT=1025
IMPORT_EXPORT_USE_TRANSACTIONS=_A
CKEDITOR_RESTRICT_BY_USER=_A
MIDDLEWARE=['debug_toolbar.middleware.DebugToolbarMiddleware','django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','corsheaders.middleware.CorsMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','django_underconstruction.middleware.UnderConstructionMiddleware']
ROOT_URLCONF='django_opd.urls'
TEMPLATES=[{_H:'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates/'],'APP_DIRS':_A,_I:{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','opd.processor.my_context','opd.processor.my_comment_count']}}]
WSGI_APPLICATION='django_opd.wsgi.application'
DB_TYPE=key['DB_TYPE']
found=False
if DB_TYPE:
	if DB_TYPE=='sqlite':found=_A;DATABASES={_B:{_J:key[_K],_C:key[_L]}}
if not found:DATABASES={_B:{_J:key[_K],_C:key[_L],'USER':key['DB_USER'],'PASSWORD':key[_D],'HOST':key['DB_HOST'],'PORT':key['DB_PORT']}}
AUTH_PASSWORD_VALIDATORS=[{_C:'django.contrib.auth.password_validation.MinimumLengthValidator'},{_C:'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='id'
TIME_ZONE='Asia/Makassar'
USE_I18N=_A
USE_L10N=_A
USE_TZ=False
STATIC_URL='static/'
tmp=key.get(_M)
STATIC_ROOT=key[_M]if tmp else os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
MEDIA_URL='/media/'
tmp=key.get(_N)
MEDIA_ROOT=key[_N]if tmp else os.path.join(BASE_DIR,'media')
SITE_ID=1
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
CKEDITOR_CONFIGS={_B:{'width':'100%',_O:'full',_P:_A,_Q:_S,'removePlugins':('exportpdf','scayt'),_R:','.join(['texttransform','html5audio','html5video','wordcount',_T,'embedsemantic','autolink','codesnippet','previewgoogledrive','previewdocument'])},_G:{_R:','.join([_T]),_P:_A,_Q:_S,_O:'Custom','toolbar_Custom':[['Source','Iframe'],['Youtube']]}}
LOCALE_PATHS=BASE_DIR/'locale',
HITCOUNT_KEEP_HIT_IN_DATABASE={'months':3}
HITCOUNT_KEEP_HIT_ACTIVE={'hours':1}
INTERNAL_IPS=['127.0.0.1']
CACHES={_B:{_H:'django_redis.cache.RedisCache','LOCATION':'redis://127.0.0.1:6379/1',_I:{'CLIENT_CLASS':'django_redis.client.DefaultClient'}}}