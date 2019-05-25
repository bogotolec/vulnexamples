from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from base64 import b32decode as decode, b32encode as encode

from vulnexamples.views import HostsLoginView, HostsRegistrationView


def get_session_id(username):
    return encode((username * 20)[:20].encode()).decode().lower()


def change_login(login):
    response = redirect('index')
    if (login is None):
        response.delete_cookie('login')
        response.delete_cookie('session_id')
    else:
        response.set_cookie('login', login, httponly=True)
        response.set_cookie('session_id', get_session_id(login), httponly=True)
    return response


def index(request):
    users = get_user_model().objects.filter(subdomain='a2_broken_auth')
    try:
        username = request.COOKIES.get('login')
        if (request.COOKIES.get('session_id') != get_session_id(username)):
            current_user = None
        else:
            current_user = get_user_model().objects.filter(login=username, subdomain='a2_broken_auth')[0]
    except (KeyError, IndexError, TypeError, AttributeError):
        current_user = None

    return render(request, 'a2_broken_auth/index.html', {'current_user': current_user, 'users': users})


class RegistrationView(HostsRegistrationView):
    subdomain = 'a2_broken_auth'

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
