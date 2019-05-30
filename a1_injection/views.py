from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.http import Http404

from vulnexamples.views import HostsLoginView, HostsRegistrationView
from .forms import RegistrationForm
from .models import AdditionalInfo


def index(request):
    return render(request, 'a1_injection/index.html',
                  {'users': get_user_model().objects.filter(subdomain='a1_injection')})


class RegistrationView(HostsRegistrationView):
    subdomain = 'a1_injection'
    form_class = RegistrationForm

    def on_success(self, request):
        data = self.form.cleaned_data
        AdditionalInfo.objects.using('a1_injection').create(
            login=data['username'],
            birthdate=data['birthdate'],
            birthdate_hidden=data['birthdate_hidden'],
            bio=data['bio']
        )
        return super().on_success(request)


class LoginView(HostsLoginView):
    subdomain = 'a1_injection'


def logout_view(request):
    logout(request)
    return redirect(reverse('index', host='a1_injection'))


def profile_view(request):
    username = request.GET.get('username')

    info = AdditionalInfo.objects.using('a1_injection').raw(
        """SELECT id, birthdate, birthdate_hidden, bio
           FROM 'a1_injection_additionalinfo'
           WHERE login='%s'
        """ % username
    )
    if (len(info) == 0):
        raise Http404("No such user")
    return render(request, 'a1_injection/profile.html', {'info': info[0]})
