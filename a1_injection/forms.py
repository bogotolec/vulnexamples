from django import forms
from django.forms import Form
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth import authenticate


class RegistrationForm(Form):
    username = forms.CharField(max_length=70)
    password = forms.CharField(widget=forms.PasswordInput)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    birthdate_hidden = forms.BooleanField(label='Hide birthdate', required=False)
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required=False)
