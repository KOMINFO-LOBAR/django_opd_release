_O='deskripsi'
_N='autofocus'
_M='placeholder'
_L='jabatan'
_K='share_count'
_J='photo'
_I='view_count'
_H=False
_G='admin'
_F='form-control'
_E='site'
_D='created_at'
_C='updated_at'
_B='__all__'
_A='class'
import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from opd.models import *
logger=logging.getLogger(__name__)
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):fields=UserCreationForm.Meta.fields+('email',)
class SocialMediaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(SocialMediaForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=social_media;fields=_B;exclude=_E,_D,_C
class InstansiForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(InstansiForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=instansi;fields=_B;exclude=_E,_G,_D,_C
class LogoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(LogoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=logo;fields=_B;exclude=_E,'photocreated_at',_C
class BannerForm(ModelForm):
	str_banner_position=forms.CharField(widget=forms.HiddenInput())
	def __init__(self,*args,**kwargs):
		super(BannerForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=banner;fields=['str_banner_position','position','link']
class MenuForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(MenuForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
		self.fields['parent'].queryset=menu.objects.filter(is_admin_menu=_H)
	class Meta:model=menu;fields=_B;exclude=_E,'is_admin_menu','href',_D,_C
class BeritaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields['isi_berita'].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=berita;fields=_B;exclude=_E,_G,_I,_K,_D,_C
class KategoriForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(KategoriForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=kategori;fields=_B;exclude=_E,'count',_D,_C
class TagsForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(TagsForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=tags;fields=_B;exclude=_E,'count',_D,_C
class PengumumanForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields['isi_pengumuman'].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=pengumuman;fields=_B;exclude=_E,_G,_I,_K,_D,_C
class ArtikelForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields['isi_artikel'].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=artikel;fields=_B;exclude=_E,_G,_I,_K,_D,_C
class PejabatForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=pejabat;fields=['nama',_L,_J];widgets={'nama':forms.TextInput(attrs={_M:'Nama Kepala Dinas / Pejabat OPD',_N:_N}),_L:forms.TextInput(attrs={_M:'Kepala Dinas OPD'})}
class DokumenForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields[_O].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=dokumen;fields=_B;exclude=_E,_G,'hits','size',_D,_C
class HalamanStatisForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields['isi_halaman'].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=halaman_statis;fields=_B;exclude=_E,_J,_I,_G,'is_edited',_D,_C
class GaleryFotoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(GaleryFotoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=galery_foto;fields=_B;exclude=_E,_G,_J,_I,_D,_C
class PopupForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(PopupForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=popup;fields=_B;exclude=_E,_G,_J,_D,_C
class GaleryLayananForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(GaleryLayananForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=galery_layanan;fields=_B;exclude=_E,_G,_J,_D,_C
class GaleryVideoForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields['embed'].required=_H
		for name in self.fields.keys():tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=galery_video;fields=_B;exclude=_E,_G,_I,_D,_C
class AgendaForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*(args),**kwargs);self.fields[_O].required=_H
		for name in self.fields.keys():
			if name=='tanggal':self.fields[name].widget.attrs.update({_A:'form-control datepicker','data-dateformat':'dd/mm/yy'})
			elif name=='jam':self.fields[name].widget.attrs.update({_A:_F,'data-autoclose':'true'})
			else:tmp=self.fields[name].widget.attrs[_A]if _A in self.fields[name].widget.attrs.keys()else'';self.fields[name].widget.attrs.update({_A:f"form-control {tmp}"})
	class Meta:model=agenda;fields=_B;exclude=_E,_G,'nama_seo',_I,_D,_C
class LinkTerkaitForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(LinkTerkaitForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=link_terkait;fields=_B;exclude=_E,'icon_awesome',_D,_C
class InfoHoaxForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(InfoHoaxForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=info_hoax;fields=_B;exclude=_D,_C
class BannerAllForm(ModelForm):
	def __init__(self,*args,**kwargs):
		super(BannerAllForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=banner_all;fields=_B;exclude=_J,_D,_C
class PhotoForm(ModelForm):
	x=forms.FloatField(widget=forms.HiddenInput());y=forms.FloatField(widget=forms.HiddenInput());width=forms.FloatField(widget=forms.HiddenInput());height=forms.FloatField(widget=forms.HiddenInput());str_file_path=forms.CharField(widget=forms.HiddenInput())
	def __init__(self,*args,**kwargs):
		super(PhotoForm,self).__init__(*(args),**kwargs)
		for name in self.fields.keys():self.fields[name].widget.attrs.update({_A:_F})
	class Meta:model=photo;fields='file_path','x','y','width','height','str_file_path';widgets={'file':forms.FileInput(attrs={'accept':'image/*'})}