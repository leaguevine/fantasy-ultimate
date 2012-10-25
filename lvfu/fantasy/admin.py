from django import forms
from django.contrib import admin

from ..utils.forms import JSONFormField

from models import Event, League, Member, Team, Player
from utils import update_player_scores, update_team_ranks


def admin_form(_model):
    class MyForm(forms.ModelForm):
        extra = JSONFormField(required=False)

        class Meta:
            model = _model
    return MyForm


class EventAdmin(admin.ModelAdmin):
    form = admin_form(Event)
    list_display = (
        'id',
        'type',
        'lv_id',
        'title',
        'description'
    )


class LeagueAdmin(admin.ModelAdmin):
    form = admin_form(League)
    list_display = (
        'id',
        'creator',
        'creation_time',
        'event',
        'title',
        'description'
    )
    date_hierarchy = 'creation_time'
    actions = ['update_scores', 'reset_scores']

    def update_scores(self, request, queryset):
        for league in queryset:
            update_player_scores(league)
            update_team_ranks(league)
        self.message_user(request, "Scores updated")
    update_scores.short_description = "Update player scores and team rankings"

    def reset_scores(self, request, queryset):
        Player.objects.get_for_leagues([l.id for l in queryset]).update(score=0)
        Team.objects.get_for_leagues([l.id for l in queryset]).update(rank=0)
        self.message_user(request, "Scores reset")
    reset_scores.short_description = "Reset player scores to 0"


class MemberAdmin(admin.ModelAdmin):
    form = admin_form(Member)
    list_display = (
        'id',
        'status',
        'creation_time',
        'fb_uid',
        'first_name',
        'last_name',
        'user',
        'league'
    )
    date_hierarchy = 'creation_time'


class TeamAdmin(admin.ModelAdmin):
    form = admin_form(Team)
    list_display = (
        'id',
        'league',
        'owner',
        'title',
        'rank'
    )
    date_hierarchy = 'creation_time'


class PlayerAdmin(admin.ModelAdmin):
    form = admin_form(Player)
    list_display = (
        'id',
        'team',
        'name',
        'lv_player_id',
        'score',
        'score_updated',
        'owner',
        'league'
    )
    date_hierarchy = 'creation_time'

    def name(self, obj):
        try:
            player = obj.extra['lv_player']
            return "%s %s" % (player['first_name'], player['last_name'])
        except (KeyError, ValueError):
            return ""


admin.site.register(Event, EventAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
