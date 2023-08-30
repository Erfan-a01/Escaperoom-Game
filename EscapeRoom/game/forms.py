from django import forms
from django.contrib.auth.models import User
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=50)
    Email = forms.EmailField()
    # Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

    # class AdminSalaryForm(forms.Form):
    # salary = forms.IntegerField()


class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = ['title', 'question_num', 'total_score']


class QuestionForm(forms.ModelForm):

    roomID = forms.ModelChoiceField(queryset=models.Room.objects.filter(), empty_label="Room Name", to_field_name="id")

    class Meta:
        model = models.Question
        fields = ['text', 'score', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
