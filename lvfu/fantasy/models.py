from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from social_auth.signals import socialauth_registered

from ..account.models import User
from ..utils.fields import JSONField
from ..utils.site import site_join_url
from ..utils.validators import choice_validator


class Event(models.Model):
    """
    An event in the real world that fantasy leagues can be tied to
    """
    TYPE_CHOICES = (
        (ur'season', u'Season'),
        (ur'tournament', u'Tournament')
    )
    TYPES = [t[0] for t in TYPE_CHOICES]

    type = models.CharField(max_length=16,
                            default='tournament',
                            choices=TYPE_CHOICES,
                            validators=[choice_validator(TYPE_CHOICES)])
    # The ID of the event in Leaguevine
    lv_id = models.IntegerField()

    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, default='')

    extra = JSONField(blank=True)

    class Meta:
        unique_together = ('type', 'lv_id')


class LeagueManager(models.Manager):
    def get_all_for_user(self, user):
        user = User.objects.get_user(user)
        return League.objects.filter(members__user=user)


class League(models.Model):
    """
    A fantasy league
    """
    # Can't really be null, just needed for migration
    event = models.ForeignKey(Event, null=True)

    creation_time = models.DateTimeField(default=datetime.utcnow,
                                         db_index=True,
                                         editable=False)

    # The user that created this league -- used for bookkeeping. All app logic
    # should use member objects.
    creator = models.ForeignKey(User)

    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, default='')

    extra = JSONField(blank=True)

    objects = LeagueManager()

    @models.permalink
    def get_absolute_url(self):
        return ('league', (), {'pk': self.pk})

    @property
    def abs_url(self):
        return site_join_url(self.get_absolute_url())


class Member(models.Model):
    """
    A member of a league. Each member belongs to exactly one league, and
    corresponds to at most one user. If a non-user is invited, they will
    only have a member object representing them. Once they sign up, their
    member object will become associated with their user object.
    """
    STATUS_CHOICES = (
        (ur'creator', u'Creator'),
        (ur'member', u'Member')
    )
    STATUSES = [t[0] for t in STATUS_CHOICES]

    # The member's status -- league creator or just regular league member
    status = models.CharField(max_length=16,
                              default='member',
                              choices=STATUS_CHOICES,
                              validators=[choice_validator(STATUS_CHOICES)])

    creation_time = models.DateTimeField(default=datetime.utcnow,
                                         editable=False)

    extra = JSONField(blank=True)

    # Only used before they sign up -- then their user and social auth objects
    # supercede these fields.
    fb_uid = models.CharField(max_length=512)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    user = models.ForeignKey(User, null=True, blank=True)
    league = models.ForeignKey(League, related_name='members')

    class Meta:
        unique_together = ('league', 'user')

    def get_first_name(self):
        return self.user.first_name if self.user else self.first_name

    def get_last_name(self):
        return self.user.last_name if self.user else self.last_name

    @property
    def full_name(self):
        return self.get_first_name() + " " + self.get_last_name()

    @property
    def profile_pic(self):
        return "https://graph.facebook.com/" + self.fb_uid + "/picture?format=square"


class Team(models.Model):
    """
    A team in a fantasy league
    """
    owner = models.ForeignKey(Member)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=2048, blank=True, default='')

    creation_time = models.DateTimeField(default=datetime.utcnow,
                                         editable=False)

    extra = JSONField(blank=True)

    @property
    def league(self):
        return self.owner.league


class PlayerManager(models.Manager):
    def get_for_league(self, league):
        return self.filter(team__owner__league=league)


class Player(models.Model):
    """
    A player on a team in a fantasy league
    """
    team = models.ForeignKey(Team)
    # The Leaguevine ID of this team/player
    lv_team_id = models.IntegerField()
    lv_player_id = models.IntegerField()

    score = models.IntegerField()
    score_updated = models.DateTimeField(default=datetime.utcnow)

    creation_time = models.DateTimeField(default=datetime.utcnow,
                                         editable=False)

    extra = JSONField(blank=True)

    objects = PlayerManager()

    @property
    def owner(self):
        return self.team.owner

    @property
    def league(self):
        return self.owner.league


@receiver(post_save, sender=League)
def create_creator_member(sender, **kwargs):
    """
    When a league is created, create the creator member
    """
    if kwargs.get('created'):
        league = kwargs['instance']
        league.members.create(user=league.creator,
                              fb_uid=league.creator.fb_uid,
                              status='creator')


@receiver(pre_save, sender=Member)
def assign_member_user(sender, **kwargs):
    "If a member's fb_uid matches a user, make sure the user is assigned."
    member = kwargs['instance']
    if not member.user:
        try:
            user = User.objects.get_by_fb_uid(member.fb_uid)
            member.user = user
        except User.DoesNotExist:
            pass


@receiver(socialauth_registered, sender=None)
def assign_user_member(sender, user, response, details, **kwargs):
    "If a new user's fb_uid matches any members, associate them"
    Member.objects.filter(fb_uid__iexact=user.fb_uid).update(user=user)
    return False
