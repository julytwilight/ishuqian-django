# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class List(models.Model):

    user      = models.ForeignKey('ishuqian.User')
    name      = models.CharField(max_length=90)
    bookmarks = models.PositiveIntegerField(default=0)
    color     = models.CharField(max_length=10, blank=True)
    addtime   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Bookmark(models.Model):

    user        = models.ForeignKey('ishuqian.User')
    list        = models.ForeignKey(List)
    title       = models.CharField(max_length=255)
    url         = models.URLField(max_length=255)
    private     = models.PositiveSmallIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    point       = models.PositiveIntegerField(default=0)
    votes       = models.PositiveIntegerField(default=0)
    addtime     = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title