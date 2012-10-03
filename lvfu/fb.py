import urllib
import urllib2

from django.conf import settings
from django.core.cache import cache


def get_app_access_token(force_refresh=False, retries=2):
    if not force_refresh:
        token = cache.get('fb.app_access_token')
        if token:
            return token

    args = {
        'grant_type': 'client_credentials',
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_API_SECRET
    }

    tries = 0
    while True:
        try:
            f = urllib.urlopen("https://graph.facebook.com/oauth/access_token",
                               data=urllib.urlencode(args))
            result = f.read()
            token = result.split('=')[1]
            cache.set('fb.app_access_token', token, 60 * 60 * 24 * 7)  # 1 week?
            return token
        except (urllib2.URLError, IndexError):
            if tries == retries:
                raise
            tries += 1
