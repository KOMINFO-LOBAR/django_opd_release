_D='username'
_C='placeholder'
_B='body'
_A='email'
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from.models import User
from opd.models import*
class CustomUserCreationForm(UserCreationForm):
	class Meta:model=User;fields=_D,_A
class CustomUserChangeForm(UserChangeForm):
	class Meta:model=User;fields=_D,_A
class CommentForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		A='class';super(CommentForm,self).__init__(*args,**kwargs)
		for name in self.fields.keys():
			if name==_B:self.fields[name].widget.attrs.update({A:'bo-1-rad-3 bocl13 size-a-15 f1-s-13 cl5 plh6 p-rl-18 p-tb-14 m-b-20'})
			else:self.fields[name].widget.attrs.update({A:'bo-1-rad-3 bocl13 size-a-16 f1-s-13 cl5 plh6 p-rl-18 m-b-20'})
	class Meta:model=comment;fields='name',_A,_B;widgets={'name':forms.TextInput(attrs={_C:'* Nama'}),_A:forms.EmailInput(attrs={_C:'* Email'}),_B:forms.Textarea(attrs={_C:'* Komentar'})}