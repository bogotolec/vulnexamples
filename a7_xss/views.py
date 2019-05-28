from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.contrib.auth import get_user_model
import re

from vulnexamples.views import HostsLoginView, HostsRegistrationView


def index(request):
    # messages = reversed(ChatMessage.objects.order_by("-created")[:10])
    # return render(request, 'a7_xss/index.html', {'messages': messages})
    return render(request, 'a7_xss/index.html')


class RegistrationView(HostsRegistrationView):
    subdomain = 'a7_xss'

    def validate(self, request):
        new_username = self.form.cleaned_data['username']
        new_password = self.form.cleaned_data['password']

        self.form.errors['username'] = self.form.errors.get('username', [])
        self.form.errors['password'] = self.form.errors.get('password', [])

        if not re.match(r'[A-Za-z0-9_\-]+', new_username):
            self.form.errors['username'] += ['Incorrect username. Username can contain only'
                                             ' english letters, digits, "_" and "-" symbols.']

        if get_user_model().objects.filter(login=new_username, subdomain=self.subdomain).exists():
            self.form.errors['username'] += ['Current user is already registered.']

        if len(new_username) > 70:
            self.form.errors['username'] += ['Username should be 70 symbols or less']

        if len(new_password) < 6:
            self.form.errors['password'] += ['Password must contain at least 6 symbols.']

        if not re.search(r'[0-9]', new_password):
            self.form.errors['password'] += ['Password must contain at least one digit.']

        if not re.search(r'[A-Z]', new_password):
            self.form.errors['password'] += ['Password must contain at least one capital letter.']

        if not re.search(r'[a-z]', new_password):
            self.form.errors['password'] += ['Password must contain at least one small letter.']

        if 'meow' not in new_password.lower():
            self.form.errors['password'] += ['Password must contain "meow"']


class LoginView(HostsLoginView):
    subdomain = 'a7_xss'


def logout_view(request):
    logout(request)
    return redirect(reverse('index', host='a7_xss'))
