from datetime import date, timedelta
import json
import urllib
import urllib2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from social_auth.db.django_models import UserSocialAuth

from fb import get_app_access_token


@login_required
def welcome(request):
    try:
        uid = request.user.social_auth.get(provider='facebook').uid
    except UserSocialAuth.DoesNotExist:
        return render("/")

    args = {
        'access_token': get_app_access_token(),
        'limit': 0
    }
    url = 'https://graph.facebook.com/%s/likes?%s' % (uid, urllib.urlencode(args))
    likes = json.load(urllib2.urlopen(url))['data']
    if settings.FACEBOOK_FAN_PAGE_ID in [l['id'] for l in likes]:
        return HttpResponseRedirect("/")
    else:
        return render(request, "welcome.html")


def index(request):
    if request.user.is_authenticated():
        return render(request, "home.html")
    else:
        return render(request, "login.html")


def fb_channel(request):
    response = HttpResponse('<script src="//connect.facebook.net/en_US/all.js"></script>',
                            mimetype='text/html')
    seconds = 31449600  # 364 days
    maxage = timedelta(seconds=seconds)
    expires = date.today() + maxage
    response['Pragma'] = 'public'
    response['Cache-Control'] = 'max-age=' + str(seconds)
    response['Expires'] = expires.strftime("%a, %d %b %Y 20:00:00 GMT")
    return response
