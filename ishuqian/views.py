# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from utils.sina import get_user_info

from models import User
from bookmark.models import Bookmark
from bookmark.models import List

def default(request):
    bookmarks = Bookmark.objects.all().order_by('-addtime')
    return render(request, 'welcome/default.html', {'bookmarks': bookmarks})

def callback(request, social):
    if social == 'weibo':
        u = get_user_info(request.GET['code'])
        u[0]['gender'] = 1 if u[0]['gender'] == 'm' else 0
        try:
            user = User.objects.get(linked_account=u[0]['id'])
            user.username         = u[0]['screen_name']
            user.location         = u[0]['location']
            user.avatar           = u[0]['avatar_large']
            user.avatar_thumbnail = u[0]['profile_image_url']
            user.gender           = u[0]['gender']
            user.access_token     = u[1].access_token
            user.expires_in       = u[1].expires_in
            user.save()

        except User.DoesNotExist:
            user = User(linked_account=u[0]['id'], username=u[0]['screen_name'],
                        location=u[0]['location'], gender=u[0]['gender'], linked_type='sina',
                        avatar=u[0]['avatar_large'], avatar_thumbnail=u[0]['profile_image_url'],
                        access_token=u[1].access_token, expires_in=u[1].expires_in)
            user.save()

            List.objects.create(name=u'默认分类', user=user)

        finally:
            request.session['id'] = user.id
            request.session['username'] = user.username
            request.session['avatar'] = user.avatar_thumbnail
    # elif social == 'qq':
    #     pass
    # else:
    #     pass

    return redirect('/')

def home(request, id=0):
    user = User.objects.get(id=request.session.get('id', None))
    if id:
        list = get_object_or_404(List, id=id)
        bookmarks = list.bookmark_set.all().order_by('-addtime')
    else:
        bookmarks = user.bookmark_set.all().order_by('-addtime')
    return render(request, 'welcome/home.html', {'user': user, 'bookmarks': bookmarks, 'list_id': int(id)})


def logout(request):
    request.session.flush()
    return redirect('/')

# return render(request, 'debug.html', {'debug': bookmarks})