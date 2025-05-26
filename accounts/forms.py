from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_image']


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
