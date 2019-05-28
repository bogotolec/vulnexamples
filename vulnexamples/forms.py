from django import forms
from django.forms import Form


class AuthenticationForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FileUploadForm(Form):
    file = forms.FileField(label='')
