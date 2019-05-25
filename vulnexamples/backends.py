from django.contrib.auth.backends import ModelBackend

from .models import HostsAuthUser


class HostsAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, subdomain=None):
        try:
            user = HostsAuthUser.objects.get(username=u'%s.%s' % (subdomain, username))
            if user.check_password(password):
                return user
        except HostsAuthUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return HostsAuthUser.objects.get(pk=user_id)
        except HostsAuthUser.DoesNotExist:
            return None
