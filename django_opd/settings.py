_M='youtube'
_L='plain-text'
_K='extraPlugins'
_J='pasteFilter'
_I='toolbarCanCollapse'
_H='toolbar'
_G='default'
_F='embed_video'
_E='localhost'
_D='127.0.0.1'
_C='NAME'
_B=False
_A=True
import os
from pathlib import Path
from decouple import Config,RepositoryEnv
from cryptography.fernet import Fernet
BASE_DIR=Path(__file__).resolve().parent.parent
env_ps1=os.environ.get('PS1')
env_opd='env_opd'
is_run_from_server=_A
if env_ps1:
	if env_opd in env_ps1:env_config=Config(RepositoryEnv(BASE_DIR/'.env.local'));print('Load Setting From env.local');is_run_from_server=_B
if is_run_from_server:env_config=Config(RepositoryEnv(BASE_DIR/'.env.server'));print('Load Setting From env.server')
DEBUG=env_config('DEBUG',default=_A,cast=bool)
UNDER_CONSTRUCTION=env_config('UNDER_CONSTRUCTION',default=_B,cast=bool)
UNDER_CONSTRUCTION_TEMPLATE='opd/construction.html'
LOGIN_REDIRECT_URL='/dashboard/dashboard'
LOGOUT_REDIRECT_URL='/'
DB_KEY=env_config('DB_KEY',default='')
fernet=Fernet(DB_KEY.encode())
DB_TMP=env_config('SECRET_KEY',default='')
SECRET_KEY=fernet.decrypt(DB_TMP.encode()).decode()
ALLOWED_HOSTS=['.lombokbaratkab.go.id',_D,_E]
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','django.contrib.sites','django.contrib.humanize',_F,'simple_open_graph','django_social_share','hitcount','opd','account','django_underconstruction','import_export','ckeditor','ckeditor_uploader','corsheaders']
CKEDITOR_UPLOAD_PATH='uploads/'
CKEDITOR_BASEPATH='/static/ckeditor/ckeditor/'
EMAIL_HOST=_E
EMAIL_PORT=1025
IMPORT_EXPORT_USE_TRANSACTIONS=_A
CKEDITOR_RESTRICT_BY_USER=_A
MIDDLEWARE=['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','corsheaders.middleware.CorsMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware','django_underconstruction.middleware.UnderConstructionMiddleware']
ROOT_URLCONF='django_opd.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'templates/'],'APP_DIRS':_A,'OPTIONS':{'context_processors':['django.template.context_processors.debug','django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages','opd.processor.my_context','opd.processor.my_comment_count']}}]
WSGI_APPLICATION='django_opd.wsgi.application'
DB_TMP=env_config('DB_PASSWORD',default='')
DB_PASSWORD=fernet.decrypt(DB_TMP.encode()).decode()
DATABASES={_G:{'ENGINE':env_config('DB_ENGINE',default='django.db.backends.mysql'),_C:env_config('DB_NAME',default='db_opd'),'USER':env_config('DB_USER',default='root'),'PASSWORD':DB_PASSWORD,'HOST':env_config('DB_HOST',default=_D),'PORT':env_config('DB_PORT',default=3306,cast=int)}}
AUTH_PASSWORD_VALIDATORS=[{_C:'django.contrib.auth.password_validation.MinimumLengthValidator'},{_C:'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='id'
TIME_ZONE='Asia/Makassar'
USE_I18N=_A
USE_L10N=_A
USE_TZ=_B
STATIC_URL='/static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
STATICFILES_DIRS=[BASE_DIR/'static']
MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR/'media'
SITE_ID=1
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
CKEDITOR_CONFIGS={_G:{'width':'100%',_H:'full',_I:_A,_J:_L,'removePlugins':('exportpdf','scayt'),_K:','.join(['texttransform','html5audio','html5video','wordcount',_M,'embedsemantic','autolink','codesnippet','previewgoogledrive','previewdocument'])},_F:{_K:','.join([_M]),_I:_A,_J:_L,_H:'Custom','toolbar_Custom':[['Source','Iframe'],['Youtube']]}}
LOCALE_PATHS=BASE_DIR/'locale',