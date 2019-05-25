from django import forms
from django.forms import Form
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth import authenticate


class AuthenticationForm(Form):
    username = forms.CharField(max_length=70)
    password = forms.CharField(widget=forms.PasswordInput)
