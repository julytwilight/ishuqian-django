# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class User(models.Model):

    linked_account   = models.CharField(max_length=100, unique=True)
    linked_type      = models.CharField(max_length=10, blank=True)
    email            = models.EmailField(max_length=90, blank=True)
    username         = models.CharField(max_length=90, unique=True)
    password         = models.CharField(max_length=50)
    gender           = models.PositiveSmallIntegerField(default=0)
    avatar           = models.CharField(max_length=255)
    avatar_thumbnail = models.CharField(max_length=255, blank=True)
    location         = models.CharField(max_length=90)
    bookmarks_count  = models.PositiveIntegerField(default=0)
    following        = models.PositiveIntegerField(default=0)
    followers        = models.PositiveIntegerField(default=0)
    point            = models.PositiveSmallIntegerField(default=0)
    state            = models.PositiveSmallIntegerField(default=0)
    access_token     = models.CharField(max_length=255, blank=True)
    expires_in       = models.CharField(max_length=255, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    last_login       = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.username