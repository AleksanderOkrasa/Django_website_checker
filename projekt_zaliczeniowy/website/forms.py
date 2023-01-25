from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import WebpageData

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False, help_text='email (not needed)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

# class EditProfileForm(forms.Form):
#     first_name = forms.CharField(max_length=30, required=False)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField()

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


