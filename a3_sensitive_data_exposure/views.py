from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django_hosts.resolvers import reverse
from django.views.defaults import bad_request, permission_denied, page_not_found, server_error
import logging
import random

from vulnexamples.views import HostsLoginView, HostsRegistrationView


def log(request, status=None):
    args = request.POST if (request.method == 'POST') else request.GET
    to_log = 'HTTP %s %s' % (request.method, request.path)
    if status is not None:
        to_log += ' [%d]' % status
    if args.dict():
        to_log += ' %s' % args.dict()
    logging.getLogger('a3_sensitive_data_exposure').debug(to_log)


def index(request):
    log(request)
    return render(request, 'a3_sensitive_data_exposure/index.html')


class RegistrationView(HostsRegistrationView):
    subdomain = 'a3_sensitive_data_exposure'

    def get(self, request):
        log(request)
        return super().get(request)

    def post(self, request):
        log(request)
        return super().post(request)


class LoginView(HostsLoginView):
    subdomain = 'a3_sensitive_data_exposure'

    def get(self, request):
        log(request)
        return super().get(request)

    def post(self, request):
        log(request)
        return super().post(request)


def logout_view(request):
    log(request)
    logout(request)
    return redirect(reverse('index', host='a3_sensitive_data_exposure'))


def robots_view(request):
    log(request)
    return render(request, 'a3_sensitive_data_exposure/robots.txt', content_type="text/plain")


def logs_view(request):
    return render(request, 'a3_sensitive_data_exposure/logs.txt',
                  {'r': random.random()}, content_type="text/plain")


def view400(request, exception):
    log(request, 400)
    return bad_request(request, exception)


def view403(request, exception):
    log(request, 403)
    return permission_denied(request, exception)


def view404(request, exception):
    log(request, 404)
    return page_not_found(request, exception)


def view500(request):
    log(request, 500)
    return server_error(request)
