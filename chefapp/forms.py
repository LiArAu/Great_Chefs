from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django_scopes import scopes_disabled
from django_scopes.forms import SafeModelChoiceField, SafeModelMultipleChoiceField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class RecipePublishForm(forms.ModelForm):
    class Meta:
        model = RecipeContent
        fields = '__all__'

class SharezoneCreationForm(forms.Form):
    prefix = 'create'
    name = forms.CharField()
    def clean_name(self):
        name = self.cleaned_data['name']
        with scopes_disabled():
            if ShareZone.objects.filter(name=name).exists():
                raise ValidationError(_('Name already taken.'))
        return name
