from django.shortcuts import redirect
from base64 import b32encode


def get_session_id(username):
    return b32encode(((username + ' ') * 20)[:20].encode()).decode().lower()


def change_login(login):
    response = redirect('index')
    if (login is None):
        response.delete_cookie('login')
        response.delete_cookie('session_id')
    else:
        response.set_cookie('login', login, httponly=True)
        response.set_cookie('session_id', get_session_id(login), httponly=True)
    return response
