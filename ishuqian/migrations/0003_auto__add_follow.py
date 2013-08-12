# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Follow'
        db.create_table(u'ishuqian_follow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fans', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ishuqian.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'ishuqian', ['Follow'])


    def backwards(self, orm):
        # Deleting model 'Follow'
        db.delete_table(u'ishuqian_follow')


    models = {
        u'ishuqian.follow': {
            'Meta': {'object_name': 'Follow'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fans': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ishuqian.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ishuqian.user': {
            'Meta': {'object_name': 'User'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'avatar_thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bookmarks_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '90', 'blank': 'True'}),
            'expires_in': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 7, 0, 0)'}),
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