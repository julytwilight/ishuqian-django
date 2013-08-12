# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # ishuqian:
    url(r'^$', 'ishuqian.views.default', name='default'),
    url(r'^callback/(?P<social>\w+)/$','ishuqian.views.callback', name='callback'),
    url(r'^signin/$', 'ishuqian.views.signin', name='signin'),
    url(r'^logout/$','ishuqian.views.logout', name='logout'),
    url(r'^home/$', 'ishuqian.views.home', name='home'),
    url(r'^home/list/(?P<id>\d+)/$', 'ishuqian.views.home', name='home_list'),

    # bookmark
    url(r'^addurl/$', 'bookmark.views.addurl', name='addurl'),
    url(r'^new/$', 'bookmark.views.new', name='new_bookmark'),
    url(r'^edit/(?P<id>\d+)/$', 'bookmark.views.edit', name='bookmark_edit'),
    url(r'^delete/(?P<id>\d+)/$', 'bookmark.views.delete', name='bookmark_delete'),
    url(r'^list/new/$', 'bookmark.views.new_list', name='new_list'),
    url(r'^list/$', 'bookmark.views.list_index', name='list'),
    url(r'^list/(?P<id>\d+)/update/$', 'bookmark.views.list_update', name='list_update'),
    url(r'^list/(?P<id>\d+)/delete/$', 'bookmark.views.list_delete', name='list_delete'),
    url(r'^list/(?P<id>\d+)/delall/$', 'bookmark.views.list_delall', name='list_delete_all'),
    url(r'^bookmarks/change/$', 'bookmark.views.bookmarks_change', name='bookmarks_change'),
    url(r'^bookmarks/delete/$', 'bookmark.views.bookmarks_delete', name='bookmarks_delete'),
    url(r'^bookmarks/import/$', 'bookmark.views.bookmarks_import', name='bookmarks_import'),
    url(r'^bookmarks/export/$', 'bookmark.views.bookmarks_export', name='bookmarks_export'),
    # url(r'^item/(?P<id>\d+)/$', 'bookmark.views.item', name='item'),
    url(r'^item/(?P<id>\d+)/reply$', 'bookmark.views.item_reply', name='item_reply'),
    url(r'^bookmark/(?P<id>\d+)/reply$', 'bookmark.views.bookmark_reply', name='bookmark_reply'),
    url(r'^bookmark/(?P<id>\d+)/go$', 'bookmark.views.bookmark_go', name='bookmark_go'),
    url(r'^item/(?P<id>\d+)/go$', 'bookmark.views.item_go', name='item_go'),

    # user
    url(r'^user/(?P<id>\d+)/$', 'ishuqian.views.user', name='user_index'),
    url(r'^user/feed/$', 'ishuqian.views.follow_bookmarks', name='user_follow_feed'),
    url(r'^user/(?P<id>\d+)/list/(?P<cate>\d+)/$', 'ishuqian.views.user', name='user_index_cate'),
    url(r'^user/follow/$', 'ishuqian.views.follow', name='user_follow'),
    url(r'^user/(?P<id>\d+)/following/$', 'ishuqian.views.following', name='user_following'),
    url(r'^user/(?P<id>\d+)/followers/$', 'ishuqian.views.followers', name='user_followers'),

    # favorite
    url(r'^favorite/(?P<id>\d+)/people/$', 'ishuqian.views.favorite_people', name='favorite_people'),


    # url(r'^ishuqian/', include('ishuqian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ staticfiles_urlpatterns()

# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += staticfiles_urlpatterns()