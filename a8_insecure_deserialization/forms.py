from django import forms
from django.forms import Form
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth import authenticate


class AddCartForm(Form):
    id = forms.IntegerField()

