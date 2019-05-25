from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model
import abc
import re
from django_hosts.resolvers import reverse_lazy, reverse

from .forms import AuthenticationForm


class MyFormView(View):
    @abc.abstractproperty
    def subdomain(self):
        return

    @abc.abstractproperty
    def template_name(self):
        return

    @abc.abstractproperty
    def form_class(self):
        return

    @abc.abstractmethod
    def validate(self, request):
        return

    @abc.abstractmethod
    def on_success(self, request):
        return

    def get(self, request):
        return self.render_form(request, self.form_class())

    def post(self, request):
        self.form = self.form_class(request.POST)

        if not self.form.is_valid():
            return self.render_form(request, self.form)

        self.validate(request)

        err = False
        for field, errs in self.form.errors.items():
            if (len(errs) != 0):
                err = True
                break
        if err:
            return self.render_form(request, self.form)

        return self.on_success(request)

    def render_form(self, request, form):
        return render(request, self.template_name, {'form': form})


class HostsRegistrationView(MyFormView):
    template_name = 'register.html'
    form_class = AuthenticationForm

    def validate(self, request):
        new_username = self.form.cleaned_data['username']
        new_password = self.form.cleaned_data['password']

        self.form.errors['username'] = self.form.errors.get('username', [])
        self.form.errors['password'] = self.form.errors.get('password', [])

        if not re.match(r'^[A-Za-z0-9_\-]+$', new_username):
            self.form.errors['username'] += ['Incorrect username. Username can contain only english letters, digits, '
                                            '"_" and "-" symbols.']

        if get_user_model().objects.filter(login=new_username, subdomain=self.subdomain).exists():
            self.form.errors['username'] += ['Current user is already registered.']

        if len(new_password) < 6:
            self.form.errors['password'] += ['Password must contain at least 6 symbols.']

        if not re.search(r'[0-9]', new_password):
            self.form.errors['password'] += ['Password must contain at least one digit.']

        if not re.search(r'[A-Z]', new_password):
            self.form.errors['password'] += ['Password must contain at least one capital letter.']

        if not re.search(r'[a-z]', new_password):
            self.form.errors['password'] += ['Password must contain at least one small letter.']

    def on_success(self, request):
            user = get_user_model().objects.create_user(
                username=self.form.cleaned_data['username'],
                password=self.form.cleaned_data['password'],
                subdomain=self.subdomain
            )
            login(request, user)
            return redirect('index')


class HostsLoginView(MyFormView):
    template_name = "login.html"
    form_class = AuthenticationForm

    def validate(self, request):
        self.user = authenticate(
            username=self.form.cleaned_data['username'],
            password=self.form.cleaned_data['password'],
            subdomain=self.subdomain
        )
        if (self.user is None):
            self.form.errors['username'] = self.form.errors.get('username', []) + ['Username or/and password is incorrect.']

    def on_success(self, request):
            login(request, self.user)
            return redirect('index')
