import json
import urllib
import urllib2

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, \
    require_POST

from social_auth.db.django_models import UserSocialAuth

from .. import lv
from ..account.models import User
from ..fb import get_app_access_token
from ..fantasy.models import Event, League, Member, Team, Player


def get_global_league():
    return League.objects.all()[0]


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
        return redirect(index)
    else:
        return render(request, "welcome.html")


def render_app(request, template, active_tab, context=None):
    context = context or {}

    app_data = context.setdefault('app_data', {})
    app_data['lvat'] = "'%s'" % lv.get_access_token()
    context['user'] = User.objects.get_user(request.user)
    context['active_tab'] = active_tab
    if not 'league' in context:
        context['league'] = get_global_league()

    return render(request, template, context)


@require_GET
def index(request):
    if request.user.is_authenticated():
        global_league = get_global_league()

        members = global_league.members.all()
        member = None
        try:
            member = members.get(user=request.user)
        except Member.DoesNotExist:
            pass

        if global_league.is_locked or (member and member.has_team):
            return redirect(league)
        else:
            return redirect(my_team)
    else:
        return render(request, "login.html")


@require_GET
@login_required
def league(request):
    league = get_global_league()

    members = league.members.all()
    member = None
    try:
        member = members.get(user=request.user)
    except Member.DoesNotExist:
        pass

    if member:
        try:
            my_team = Team.objects.get(owner=member)
        except Team.DoesNotExist:
            my_team = None
    else:
        my_team = None

    teams = (Team.objects.get_for_league(league)
                         .filter(owner__league=league)
                         .order_by('rank', 'id')
                         .prefetch_related('owner__user__social_auth')
                         .all())

    top_players = (Player.objects.get_for_league(league)
                                 .distinct('lv_player_id', 'score')
                                 .order_by('-score')
                                 .all())

    count = 20

    return render_app(request, 'league.html', "league", {
        'league': league,
        'member': member,
        'teams': teams[:count],
        'total_teams': teams.count(),
        'my_team': my_team,
        'top_players': top_players[:count]
    })


@require_http_methods(['GET', 'POST'])
@login_required
def my_team(request):
    league = get_global_league()

    members = league.members.all()
    member = None
    try:
        member = members.get(user=request.user)
    except Member.DoesNotExist:
        pass

    if request.method == 'GET':
        if member and member.has_team:
            return render_app(request, 'team.html', "team", {
                'league': league,
                'member': member
            })
        elif league.is_locked:
            return render_app(request, 'league_locked.html', "league")
        else:
            return render_app(request, 'create_team.html', "team", {
                'league': league
            })
    else:
        if league.is_locked:
            return HttpResponseForbidden("League is locked")

        title = request.POST['title']
        player_ids = [int(request.POST['player_%d' % i]) for i in range(7)]

        # Fetch a copy of the player objects to store in the JSON fields
        players = lv.GetListRequest("/players/", player_ids=lv.make_list_qp(player_ids)).get_all()

        created = True
        if member:
            if member.has_team:
                created = False
                member.team.delete()
        else:
            member = league.members.create(user=request.user)

        team = Team.objects.create(title=title, owner=member)
        team.players.bulk_create([Player(team=team,
                                         lv_player_id=player['id'],
                                         extra=json.dumps({'lv_player': player})) for player in players])

        return render_app(request, 'team.html', "team", {
            'league': league,
            'member': Member.objects.get(pk=member.pk),
            'created': created
        })


@require_GET
@login_required
def modify_team(request):
    league = get_global_league()

    members = league.members.all()
    member = None
    try:
        member = members.get(user=request.user)
    except Member.DoesNotExist:
        pass

    if member and member.has_team:
        return render_app(request, 'create_team.html', "team", {
            'league': league,
            'team': member.team,
            'players': member.team.players.all()
        })
    else:
        return redirect(my_team)


@require_GET
@login_required
def rules(request):
    return render_app(request, 'rules.html', "rules")


@require_http_methods(['GET', 'POST'])
@login_required
def new_league(request):
    if request.method == 'GET':
        return render_app(request, 'new_league.html', {
            'events': Event.objects.all()
        })
    else:
        title = request.POST['title']
        event_id = int(request.POST['event_id'])
        league = League.objects.create(event=Event.objects.get(pk=event_id),
                                       title=title,
                                       creator=request.user)
        return redirect(league)


@require_http_methods(['GET', 'POST'])
@login_required
def _league(request, pk):
    league = get_object_or_404(League, pk=pk)

    members = league.members.all()
    member = None
    try:
        member = members.get(user=request.user)
    except Member.DoesNotExist:
        pass

    if request.method == 'GET':
        if member and member.has_team:
            return render_app(request, 'league.html', {
                'league': league,
                'member': member,
                'members': members
            })
        else:
            return render_app(request, 'join_league.html', {
                'league': league,
                'members': members
            })
    else:
        if not 'action' in request.POST or request.POST['action'] != 'invite':
            return HttpResponseBadRequest();

        if not member:
            return HttpResponseForbidden()

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


#
# Fragments
#
@require_GET
def fragment_roster(request):
    team_id = request.GET['team_id']
    team = Team.objects.get(pk=team_id)
    return render(request, 'fragments/roster.html', {
        'team': team
    })


@require_POST
@login_required
@csrf_exempt
def fragment_team_rows(request):
    league = get_global_league()

    members = league.members.all()
    member = None
    try:
        member = members.get(user=request.user)
    except Member.DoesNotExist:
        pass

    friend_ids = [uid for uid in request.POST['fb_uids'].split(",") if uid]
    if member:
        uid = member.get_fb_uid()
        if uid not in friend_ids:
            friend_ids.append(uid)

    teams = (Team.objects.get_for_league(league)
                         .filter(owner__league=league)
                         .filter(Q(owner__fb_uid__in=friend_ids) |
                                 Q(owner__user__social_auth__provider='facebook',
                                   owner__user__social_auth__uid__in=friend_ids))
                         .order_by('rank', 'id')
                         .prefetch_related('owner__user__social_auth')
                         .all())

    return render(request, 'fragments/team_rows.html', {
        'league': league,
        'teams': teams,
        'member': member
    })
