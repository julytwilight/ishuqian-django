# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'ishuqian_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('linked_account', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('linked_type', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=90, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=90)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('avatar', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('avatar_thumbnail', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('bookmarks_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('following', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('followers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('point', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('state', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 18, 0, 0))),
        ))
        db.send_create_signal(u'ishuqian', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'ishuqian_user')


    models = {
        u'ishuqian.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'avatar_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bookmarks_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '90', 'blank': 'True'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 18, 0, 0)'}),
            'linked_account': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'linked_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '90'})
        }
    }

    complete_apps = ['ishuqian']