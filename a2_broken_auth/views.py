from django.contrib.auth import get_user_model
from django.shortcuts import render

from vulnexamples.views import HostsLoginView, HostsRegistrationView
from .auth_helpers import get_session_id, change_login


def index(request):
    users = get_user_model().objects.filter(subdomain='a2_broken_auth')
    try:
        username = request.COOKIES.get('login')
        if (request.COOKIES.get('session_id') != get_session_id(username)):
            current_user = None
        else:
            current_user = get_user_model().objects.get(login=username,
                                                        subdomain='a2_broken_auth')
    except (KeyError, IndexError, TypeError, AttributeError):
        current_user = None

    return render(request, 'a2_broken_auth/index.html',
                  {'current_user': current_user, 'users': users})


class RegistrationView(HostsRegistrationView):
    subdomain = 'a2_broken_auth'

    def validate(self, request):
        super().validate(request)
        if len(self.form.cleaned_data['username']) > 20:
            self.form.errors['username'] += ['Username should be 20 symbols or less']

    def on_success(self, request):
        user = get_user_model().objects.create_user(
            username=self.form.cleaned_data['username'],
            password=self.form.cleaned_data['password'],
            subdomain=self.subdomain
        )

        return change_login(user.login)


class LoginView(HostsLoginView):
    subdomain = 'a2_broken_auth'

    def on_success(self, request):
        return change_login(self.user.login)


def logout_view(request):
    return change_login(None)
