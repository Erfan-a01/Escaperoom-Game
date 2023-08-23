from django import forms
from django.contrib.auth.models import User
from . import player_models


class PlayerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class PLayerForm(forms.ModelForm):
    class Meta:
        model = player_models.Player
        fields = ['address', 'mobile']
