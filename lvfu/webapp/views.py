import json
import urllib
import urllib2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from social_auth.db.django_models import UserSocialAuth

from ..fb import get_app_access_token
from ..fantasy.models import League, Member


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
        leagues = League.objects.get_all_for_user(request.user)
        if leagues:
            return render(request, "home.html", {'leagues': leagues})
        else:
            return render(request, "getstarted.html")
    else:
        return render(request, "login.html")


def render_league(request, league_pk, template, context=None):
    league = get_object_or_404(League, pk=league_pk)
    try:
        member = league.members.get(user=request.user)
    except Member.DoesNotExist:
        return redirect_to_login(league.get_absolute_url())

    context = context or {}
    context['league'] = league
    context['member'] = member

    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
@login_required
def new_league(request):
    if request.method == 'GET':
        return render(request, 'new_league.html')
    else:
        title = request.POST['title']
        league = League.objects.create(title=title,
                                       lv_event_id=20063,
                                       creator=request.user)
        return redirect(league)


@require_http_methods(['GET', 'POST'])
@login_required
def league(request, pk):
    league = get_object_or_404(League, pk=pk)

    members = league.members.all()
    member = [m for m in members if m.user == request.user]
    if not member:
        return redirect_to_login(league.get_absolute_url())
    member = member[0]

    if request.method == 'GET':
        return render(request, 'league.html', {
            'league': league,
            'member': member,
            'members': members
        })
    else:
        if not 'action' in request.POST or request.POST['action'] != 'invite':
            return HttpResponseBadRequest();

        uids = request.POST['uids'].split(",")
        first_names = request.POST['first_names'].split(",")
        last_names = request.POST['last_names'].split(",")

        existing_uids = [m.fb_uid for m in members]

        objs = [Member(league=league,
                       fb_uid=uid,
                       first_name=first_names[i],
                       last_name=last_names[i]) for i, uid in enumerate(uids) if uid not in existing_uids]
        league.members.bulk_create(objs)
        return redirect(league)
