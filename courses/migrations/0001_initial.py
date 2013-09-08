# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table('courses_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('distance', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('courses', ['Course'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table('courses_course')


    models = {
        'courses.course': {
            'Meta': {'object_name': 'Course'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'distance': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['courses']