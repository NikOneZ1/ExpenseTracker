from django import forms
from django.contrib.auth.models import User
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm

class UserRegistration(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'username']
