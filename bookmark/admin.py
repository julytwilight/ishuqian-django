# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Bookmark, Item, List

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user',)

class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'user',)

admin.site.register(Item, ItemAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Bookmark, BookmarkAdmin)