from django import forms
from django.forms import Form


class CreateNoteForm(Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10}), max_length=500)
