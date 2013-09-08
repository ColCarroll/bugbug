# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Result'
        db.create_table('results_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meets.Meet'])),
            ('time', self.gf('django.db.models.fields.FloatField')()),
            ('runner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['runners.Runner'])),
        ))
        db.send_create_signal('results', ['Result'])


    def backwards(self, orm):
        # Deleting model 'Result'
        db.delete_table('results_result')


    models = {
        'courses.course': {
            'Meta': {'object_name': 'Course'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'distance': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'meets.meet': {
            'Meta': {'object_name': 'Meet'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meet_name': ('django.db.models.fields.CharField', [], {'max_length': '240'})
        },
        'results.result': {
            'Meta': {'object_name': 'Result'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['meets.Meet']"}),
            'runner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['runners.Runner']"}),
            'time': ('django.db.models.fields.FloatField', [], {})
        },
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

    complete_apps = ['results']