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
        # We only do Facebook authentication, so there should only ever be one
        # social_auth object. Doing it this way allows prefetch_related calls
        # (...user__social_auth) at a higher level to function as expected,
        # and shouldn't really incur any additional overhead in other cases.
        auth = [a for a in self.social_auth.all() if a.provider == 'facebook']
        return auth[0].uid

    @property
    def profile_pic(self):
        return "https://graph.facebook.com/" + self.fb_uid + "/picture?format=square"
