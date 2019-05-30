from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.http import Http404


from vulnexamples.views import HostsLoginView, HostsRegistrationView, MyFormView
from .models import Note
from .forms import CreateNoteForm


def index(request):
    notes = None
    if request.user.is_authenticated:
        notes = Note.objects.filter(author=request.user.login)
    return render(request, 'a5_broken_access_control/index.html', {'notes': notes})


class RegistrationView(HostsRegistrationView):
    subdomain = 'a5_broken_access_control'


class LoginView(HostsLoginView):
    subdomain = 'a5_broken_access_control'


def logout_view(request):
    logout(request)
    return redirect(reverse('index', host='a5_broken_access_control'))


class NewNoteView(MyFormView):
    auth_needed = True
    template_name = "a5_broken_access_control/new_note.html"
    form_class = CreateNoteForm

    def on_success(self, request):
        data = self.form.cleaned_data
        note = Note.objects.create(
            author=request.user.login,
            title=data['title'],
            text=data['text'],
        )
        return redirect(reverse('note', host='a5_broken_access_control') + '?id=' + str(note.id))


def note_view(request):
    try:
        note = Note.objects.get(id=request.GET.get('id'))
    except (Note.DoesNotExist, ValueError):
        raise Http404("No such note")
    return render(request, 'a5_broken_access_control/note.html', {'note': note})
