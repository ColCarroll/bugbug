# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Meet'
        db.create_table('meets_meet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('meet_name', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'])),
        ))
        db.send_create_signal('meets', ['Meet'])


    def backwards(self, orm):
        # Deleting model 'Meet'
        db.delete_table('meets_meet')


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
        }
    }

    complete_apps = ['meets']