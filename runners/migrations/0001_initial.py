# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Runner'
        db.create_table('runners_runner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('class_year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('runners', ['Runner'])

        # Adding M2M table for field teams on 'Runner'
        m2m_table_name = db.shorten_name('runners_runner_teams')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('runner', models.ForeignKey(orm['runners.runner'], null=False)),
            ('team', models.ForeignKey(orm['teams.team'], null=False))
        ))
        db.create_unique(m2m_table_name, ['runner_id', 'team_id'])


    def backwards(self, orm):
        # Deleting model 'Runner'
        db.delete_table('runners_runner')

        # Removing M2M table for field teams on 'Runner'
        db.delete_table(db.shorten_name('runners_runner_teams'))


    models = {
        'runners.runner': {
            'Meta': {'object_name': 'Runner'},
            'class_year': ('django.db.models.fields.IntegerField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['teams.Team']"})
        },
        'teams.team': {
            'Meta': {'object_name': 'Team'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['runners']