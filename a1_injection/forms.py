from django import forms
from django.forms import Form


class RegistrationForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    birthdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    birthdate_hidden = forms.BooleanField(label='Hide birthdate', required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}),
                          required=False, max_length=500)
