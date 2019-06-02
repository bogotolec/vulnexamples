from django import forms
from django.forms import Form


class HashForm(Form):
    text = forms.CharField(label='Text to hash')
    times = forms.CharField(label='How many times to hash', initial=1,
                            widget=forms.NumberInput(attrs={'min': 0}))
