# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Follow.fans'
        db.add_column(u'ishuqian_follow', 'fans',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='f+', to=orm['ishuqian.User']),
                      keep_default=False)

        # Adding field 'Follow.hero'
        db.add_column(u'ishuqian_follow', 'hero',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='h+', to=orm['ishuqian.User']),
                      keep_default=False)

        # Removing M2M table for field hero on 'Follow'
        db.delete_table('ishuqian_follow_hero')

        # Removing M2M table for field fans on 'Follow'
        db.delete_table('ishuqian_follow_fans')


    def backwards(self, orm):
        # Deleting field 'Follow.fans'
        db.delete_column(u'ishuqian_follow', 'fans_id')

        # Deleting field 'Follow.hero'
        db.delete_column(u'ishuqian_follow', 'hero_id')

        # Adding M2M table for field hero on 'Follow'
        db.create_table(u'ishuqian_follow_hero', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('follow', models.ForeignKey(orm[u'ishuqian.follow'], null=False)),
            ('user', models.ForeignKey(orm[u'ishuqian.user'], null=False))
        ))
        db.create_unique(u'ishuqian_follow_hero', ['follow_id', 'user_id'])

        # Adding M2M table for field fans on 'Follow'
        db.create_table(u'ishuqian_follow_fans', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('follow', models.ForeignKey(orm[u'ishuqian.follow'], null=False)),
            ('user', models.ForeignKey(orm[u'ishuqian.user'], null=False))
        ))
        db.create_unique(u'ishuqian_follow_fans', ['follow_id', 'user_id'])


    models = {
        u'ishuqian.follow': {
            'Meta': {'object_name': 'Follow'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fans': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'f+'", 'to': u"orm['ishuqian.User']"}),
            'hero': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'h+'", 'to': u"orm['ishuqian.User']"}),
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