from django.contrib.auth.models import User as BaseUser, \
    UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def get_user(self, user):
        "Downcasts a Django user to our proxy to access our methods."
        if user.is_authenticated() and type(user) != User:
            # It's probably a django.contrib.auth.models.User
            return User.objects.get(pk=user.pk)
        else:
            return user

    def get_by_fb_uid(self, uid):
        return self.get(social_auth__provider='facebook',
                        social_auth__uid__iexact=uid)


class User(BaseUser):
    class Meta:
        proxy = True

    objects = UserManager()

    @property
    def fb_uid(self):
        return self.social_auth.get(provider='facebook').uid

    @property
    def profile_pic(self):
        return "https://graph.facebook.com/" + self.fb_uid + "/picture?format=square"
