_M='autofocus'
_L='placeholder'
_K='photocreated_at'
_J='share_count'
_I='photo'
_H='view_count'
_G='admin'
_F='created_at'
_E='site'
_D='updated_at'
_C='__all__'
_B='form-control'
_A='class'
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from opd.models import *
import logging
logger=logging.getLogger(__name__)
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):fields=UserCreationForm.Meta.fields+('email',)
class SocialMediaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(SocialMediaForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=social_media;fields=_C;exclude=_E,_F,_D
class InstansiForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(InstansiForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=instansi;fields=_C;exclude=_E,_G,_F,_D
class LogoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(LogoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=logo;fields=_C;exclude=_E,_K,_D
class BannerForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(BannerForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=banner;fields=_C;exclude=_E,_K,_D
class MenuForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(MenuForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
		self.fields['parent'].queryset=menu.objects.filter(is_admin_menu=False)
	class Meta:model=menu;fields=_C;exclude=_E,'is_admin_menu','href',_F,_D
class BeritaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(BeritaForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=berita;fields=_C;exclude=_E,_G,_H,_J,_F,_D
class KategoriForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(KategoriForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=kategori;fields=_C;exclude=_E,'count',_F,_D
class TagsForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(TagsForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=tags;fields=_C;exclude=_E,'count',_F,_D
class PengumumanForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(PengumumanForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=pengumuman;fields=_C;exclude=_E,_G,_H,_J,_F,_D
class ArtikelForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(ArtikelForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=artikel;fields=_C;exclude=_E,_G,_H,_J,_F,_D
class PejabatForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(PejabatForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=pejabat;fields=_C;exclude=_E,_G,'is_default',_F,_D;widgets={'nama':forms.TextInput(attrs={_L:'Nama Kepala Dinas / Pejabat OPD',_M:_M}),'jabatan':forms.TextInput(attrs={_L:'Kepala Dinas OPD'})}
class DokumenForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(DokumenForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=dokumen;fields=_C;exclude=_E,_G,'hits','size',_F,_D
class HalamanStatisForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(HalamanStatisForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=halaman_statis;fields=_C;exclude=_E,_I,_H,_G,'is_edited',_F,_D
class GaleryFotoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(GaleryFotoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=galery_foto;fields=_C;exclude=_E,_G,_I,_H,_F,_D
class PopupForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(PopupForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=popup;fields=_C;exclude=_E,_G,_I,_F,_D
class GaleryLayananForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(GaleryLayananForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=galery_layanan;fields=_C;exclude=_E,_G,_I,_F,_D
class GaleryVideoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(GaleryVideoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=galery_video;fields=_C;exclude=_E,_G,_H,_F,_D
class AgendaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(AgendaForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():
			if name=='tanggal':self.fields[name].widget.attrs.update({_A:'form-control datepicker','data-dateformat':'dd/mm/yy'})
			elif name=='jam':self.fields[name].widget.attrs.update({_A:_B,'data-autoclose':'true'})
			else:self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=agenda;fields=_C;exclude=_E,_G,'nama_seo',_H,_F,_D
class LinkTerkaitForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(LinkTerkaitForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=link_terkait;fields=_C;exclude=_E,'icon_awesome',_F,_D
class InfoHoaxForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(InfoHoaxForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=info_hoax;fields=_C;exclude=_F,_D
class BannerAllForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(BannerAllForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=banner_all;fields=_C;exclude=_I,_F,_D
class PhotoForm(ModelForm):
	x=forms.FloatField(widget=forms.HiddenInput());y=forms.FloatField(widget=forms.HiddenInput());width=forms.FloatField(widget=forms.HiddenInput());height=forms.FloatField(widget=forms.HiddenInput());str_file_path=forms.CharField(widget=forms.HiddenInput())
	def __init__(self,*args,**kwargs):
		super(PhotoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_B})
	class Meta:model=photo;fields='file_path','x','y','width','height','str_file_path';widgets={'file':forms.FileInput(attrs={'accept':'image/*'})}