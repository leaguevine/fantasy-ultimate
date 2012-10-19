# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'League'
        db.create_table('fantasy_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.CharField')(default='season', max_length=16)),
            ('lv_event_id', self.gf('django.db.models.fields.IntegerField')()),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=2048, blank=True)),
            ('extra', self.gf('lvfu.utils.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal('fantasy', ['League'])

        # Adding model 'Member'
        db.create_table('fantasy_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='member', max_length=16)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('extra', self.gf('lvfu.utils.fields.JSONField')(blank=True)),
            ('fb_uid', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fantasy.League'])),
        ))
        db.send_create_signal('fantasy', ['Member'])

        # Adding unique constraint on 'Member', fields ['league', 'user']
        db.create_unique('fantasy_member', ['league_id', 'user_id'])

        # Adding model 'Team'
        db.create_table('fantasy_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fantasy.Member'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=2048, blank=True)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('extra', self.gf('lvfu.utils.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal('fantasy', ['Team'])

        # Adding model 'Player'
        db.create_table('fantasy_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fantasy.Team'])),
            ('lv_team_id', self.gf('django.db.models.fields.IntegerField')()),
            ('lv_player_id', self.gf('django.db.models.fields.IntegerField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('score_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('extra', self.gf('lvfu.utils.fields.JSONField')(blank=True)),
        ))
        db.send_create_signal('fantasy', ['Player'])


    def backwards(self, orm):
        # Removing unique constraint on 'Member', fields ['league', 'user']
        db.delete_unique('fantasy_member', ['league_id', 'user_id'])

        # Deleting model 'League'
        db.delete_table('fantasy_league')

        # Deleting model 'Member'
        db.delete_table('fantasy_member')

        # Deleting model 'Team'
        db.delete_table('fantasy_team')

        # Deleting model 'Player'
        db.delete_table('fantasy_player')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fantasy.league': {
            'Meta': {'object_name': 'League'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2048', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'default': "'season'", 'max_length': '16'}),
            'extra': ('lvfu.utils.fields.JSONField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lv_event_id': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'fantasy.member': {
            'Meta': {'unique_together': "(('league', 'user'),)", 'object_name': 'Member'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'extra': ('lvfu.utils.fields.JSONField', [], {'blank': 'True'}),
            'fb_uid': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.League']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'member'", 'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'fantasy.player': {
            'Meta': {'object_name': 'Player'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'extra': ('lvfu.utils.fields.JSONField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lv_player_id': ('django.db.models.fields.IntegerField', [], {}),
            'lv_team_id': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'score_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Team']"})
        },
        'fantasy.team': {
            'Meta': {'object_name': 'Team'},
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2048', 'blank': 'True'}),
            'extra': ('lvfu.utils.fields.JSONField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fantasy.Member']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['fantasy']