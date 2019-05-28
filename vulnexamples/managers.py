from django.contrib.auth.base_user import BaseUserManager


class HostsAuthManager(BaseUserManager):

    def create_user(self, username, password, subdomain):
        user = self.model(
            username=('%s.%s' % (subdomain, username)),
            login=username,
            subdomain=subdomain
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, subdomain):
        self.create_user(username, password, subdomain)
