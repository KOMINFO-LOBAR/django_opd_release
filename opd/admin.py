_W='is_frontend'
_V='rel_path'
_U='script'
_T='tanggal'
_S='file_path'
_R='order_menu'
_Q='parent'
_P='active'
_O='created_at'
_N='kategori'
_M='jabatan'
_L='view_count'
_K='photo'
_J='link'
_I='jenis'
_H='position'
_G='-updated_at'
_F='admin'
_E='name'
_D='judul'
_C='updated_at'
_B='site'
_A='nama'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from import_export.admin import ImportExportModelAdmin
class commentAdmin(admin.ModelAdmin):
	list_display=_E,'body','post',_O,_P;list_filter=_P,_O;search_fields=_E,'email','body';actions=['approve_comments']
	def approve_comments(self,request,queryset):queryset.update(active=True)
class menuAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_Q,'is_admin_menu','is_master_menu','is_statis_menu';list_display=[_Q,_A,'href','icon',_R,_C];search_fields=_A,;ordering='-is_admin_menu','parent_id',_R
class kategoriAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_A,_C];search_fields=_A,;ordering=_A,
class beritaAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D,_N;list_display=[_D,_N,_F,_L,_C];search_fields=_D,;ordering=_G,
class instansiKategoriAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_A,;list_display=[_A,_C];search_fields=_A,;ordering=_A,
class instansiAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A,_F;list_display=[_B,_A,'alamat',_N,'histats',_C];search_fields=_A,;ordering=_A,
class social_mediaAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_I;list_display=[_B,_I,_J,_C];search_fields=_J,;ordering=_I,
class logoAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_H;list_display=[_B,_H,_K,_C];search_fields=_H,;ordering=_H,
class bannerAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_H;list_display=[_B,_H,_K,_J,_C];search_fields=_H,;ordering=_H,
class banner_allAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_E,;list_display=[_E,_K,_J,_C];search_fields=_E,;ordering=_E,
class photoAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_I;list_display=[_B,_I,_S,_C];search_fields=_I,;ordering=_I,
class pengumumanAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D,_F;list_display=[_B,_D,_F,_C];search_fields=_D,;ordering=_G,
class artikelAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D,_F;list_display=[_B,_D,_F,_C];search_fields=_D,;ordering=_G,
class dokumenAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A,_F;list_display=[_B,_A,_S,_F,_C];search_fields=_A,;ordering=_G,
class link_terkaitAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_A,_J,_C];search_fields=_A,;ordering=_A,
class InfoHoaxAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_E,;list_display=[_E,_J,_C];search_fields=_E,;ordering=_E,
class galery_fotoAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D;list_display=[_B,_D,_K,_L,_C];search_fields=_D,;ordering=_G,
class galery_videoAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D;list_display=[_B,_D,'embed','embed_video',_L,_C];search_fields=_D,;ordering=_G,
class tagsAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_A,_C];search_fields=_A,;ordering=_A,
class statistikAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,'ip';list_display=[_B,'ip','hits',_T];search_fields='ip',;ordering='-tanggal',
class pejabatAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_M;list_display=[_A,_M,_K,_C];search_fields=_A,;ordering='jabatan_index',
class no_pentingAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_M;list_display=[_B,_A,_M,'nomor',_C];search_fields=_A,;ordering=_A,
class halaman_statisAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D;list_display=[_B,_D,_L,'menu',_C];search_fields=_D,;ordering=_G,
class page_widgetAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_A,_U,_F,_C];search_fields=_A,;ordering=_A,
class agendaAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_B,_A,_F,'lokasi',_T,'jam','penyelenggara'];search_fields=_A,;ordering=_G,
class page_rssAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_A;list_display=[_A,_U,_F,_C];search_fields=_A,;ordering=_A,
class galery_layananAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_B,_D;list_display=[_B,_D,_K,_F,_C];search_fields=_D,;ordering=_G,
class TemplateAdmin(ImportExportModelAdmin,admin.ModelAdmin):list_filter=_E,_V,_W;list_display=[_E,_V,'get_sites',_W,_C];search_fields=_E,;ordering='-is_frontend',_C
admin.site.register(comment,commentAdmin)
admin.site.register(menu,menuAdmin)
admin.site.register(kategori,kategoriAdmin)
admin.site.register(berita,beritaAdmin)
admin.site.register(instansi_kategori,instansiKategoriAdmin)
admin.site.register(instansi,instansiAdmin)
admin.site.register(social_media,social_mediaAdmin)
admin.site.register(logo,logoAdmin)
admin.site.register(banner,bannerAdmin)
admin.site.register(banner_all,banner_allAdmin)
admin.site.register(photo,photoAdmin)
admin.site.register(pengumuman,pengumumanAdmin)
admin.site.register(artikel,artikelAdmin)
admin.site.register(dokumen,dokumenAdmin)
admin.site.register(link_terkait,link_terkaitAdmin)
admin.site.register(info_hoax,InfoHoaxAdmin)
admin.site.register(galery_foto,galery_fotoAdmin)
admin.site.register(galery_video,galery_videoAdmin)
admin.site.register(tags,tagsAdmin)
admin.site.register(statistik,statistikAdmin)
admin.site.register(pejabat,pejabatAdmin)
admin.site.register(no_penting,no_pentingAdmin)
admin.site.register(halaman_statis,halaman_statisAdmin)
admin.site.register(page_widget,page_widgetAdmin)
admin.site.register(agenda,agendaAdmin)
admin.site.register(page_rss,page_rssAdmin)
admin.site.register(galery_layanan,galery_layananAdmin)
admin.site.register(Template,TemplateAdmin)