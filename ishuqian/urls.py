# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # ishuqian:
    url(r'^$', 'ishuqian.views.default', name='default'),
    url(r'^home/$', 'ishuqian.views.home', name='home'),
    url(r'^home/list/(?P<id>\d+)/$', 'ishuqian.views.home', name='home_list'),
    url(r'^callback/(?P<social>\w+)/$','ishuqian.views.callback', name='callback'),
    url(r'^logout/$','ishuqian.views.logout', name='logout'),

    # bookmark
    url(r'^addurl/$', 'bookmark.views.addurl', name='addurl'),
    url(r'^new/$', 'bookmark.views.new', name='new_bookmark'),
    url(r'^list/new/$', 'bookmark.views.new_list', name='new_list'),

    # url(r'^ishuqian/', include('ishuqian.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
