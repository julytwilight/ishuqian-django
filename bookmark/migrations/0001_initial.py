# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'List'
        db.create_table(u'bookmark_list', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ishuqian.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('bookmarks', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'bookmark', ['List'])

        # Adding model 'Bookmark'
        db.create_table(u'bookmark_bookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ishuqian.User'])),
            ('list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmark.List'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('private', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('views_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('point', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('addtime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'bookmark', ['Bookmark'])


    def backwards(self, orm):
        # Deleting model 'List'
        db.delete_table(u'bookmark_list')

        # Deleting model 'Bookmark'
        db.delete_table(u'bookmark_bookmark')


    models = {
        u'bookmark.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmark.List']"}),
            'point': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'private': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ishuqian.User']"}),
            'views_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'bookmark.list': {
            'Meta': {'object_name': 'List'},
            'addtime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'bookmarks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ishuqian.User']"})
        },
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

    complete_apps = ['bookmark']