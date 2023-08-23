from django import forms
from django.contrib.auth.models import User
from . import player_models
from accounts import owner_models


class OwnerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class OwnerForm(forms.ModelForm):
    class Meta:
        model = owner_models.Owner
        fields = ['address', 'mobile']
