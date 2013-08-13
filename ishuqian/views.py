# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.db import connection

from utils.sina import get_user_info
from utils import login_required
from models import User, Follow
from bookmark.models import Bookmark, List, Item


def default(request):
    items = Item.objects.exclude(title='').order_by('-addtime')
    return render(request, 'welcome/default.html', {'items': items})


# 查看收藏书签的用户
def favorite_people(request, id):
    item = get_object_or_404(Item, id=id)
    people = item.bookmark_set.exclude(private=1)
    return render(request, 'favorite/people.html', {'people': people, 'item': item})


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
    if request.session.get('redirect_url', None):
        redirect_url = request.session.get('redirect_url', None)
        del request.session['redirect_url']
        return redirect('/addurl?url=' + redirect_url)
    return redirect('/')


def signin(request):
    if request.session.get('id', None):
        return redirect('default')
    return render(request, 'welcome/signin.html')


def logout(request):
    request.session.flush()
    return redirect('/')


@login_required
def home(request, id=0):
    user = User.objects.get(id=request.session.get('id', None))
    if id:
        list = get_object_or_404(List, id=id)
        bookmarks = list.bookmark_set.all().order_by('-updatetime')
    else:
        bookmarks = user.bookmark_set.all().order_by('-updatetime')
    return render(request, 'welcome/home.html', {'user': user, 'bookmarks': bookmarks, 'list_id': int(id)})

# return render(request, 'debug.html', {'debug': bookmarks})


@login_required
def home_public(request):
    user = User.objects.get(id=request.session.get('id', None))
    bookmarks = user.bookmark_set.filter(private=0).order_by('-updatetime')
    return render(request, 'welcome/home.html', {'user': user, 'bookmarks': bookmarks, 'list_id': 'public'})


@login_required
def home_private(request):
    user = User.objects.get(id=request.session.get('id', None))
    bookmarks = user.bookmark_set.filter(private=1).order_by('-updatetime')
    return render(request, 'welcome/home.html', {'user': user, 'bookmarks': bookmarks, 'list_id': 'private'})


# user
def user(request, id, cate=None):
    user = get_object_or_404(User, id=id)
    if cate is None:
        bookmarks = user.bookmark_set.order_by('-updatetime')
        list_id = 0
    else:
        cate = List.objects.get(id=cate, user=user)
        bookmarks = cate.bookmark_set.order_by('-updatetime')
        list_id = cate.id

    fans = request.session.get('id',None)
    if fans is None or fans == user.id:
        is_follow = 'none'
    else:
        try:
            f = Follow.objects.get(fans_id=fans, hero=user)
        except Follow.DoesNotExist:
            is_follow = 'no'
        else:
            is_follow = 'yes'
    # list_id = cate if cate is None else 0
    return render(request, 'user/show.html', {'user': user, 'bookmarks': bookmarks, 'list_id': list_id, 'follow': is_follow})


# 查看关注的人的书签
@login_required
def follow_bookmarks(request):
    user = get_object_or_404(User, id=request.session.get('id', None))
    follows = user.fans.all()
    bookmarks = Bookmark.objects.filter(user__in=[i.hero for i in follows]).exclude(private=1).order_by('-addtime')
    return render(request, 'user/follow_bookmarks.html', {'user': user, 'bookmarks': bookmarks, 'count': bookmarks.count()})


# 关注和取消关注
@csrf_exempt
@login_required
def follow(request):
    if request.method == 'POST':
        try:
            fans = User.objects.get(id=request.session.get('id', None))
            hero = User.objects.get(id=request.POST.get('id', None))
        except User.DoesNotExist:
            json = simplejson.dumps({'error': 1, 'message': u'r u kidding?'})
        else:
            try:
                relation = Follow.objects.get(fans=fans, hero=hero)
            except Follow.DoesNotExist:
                Follow.objects.create(fans=fans, hero=hero)
                status = 'followed'
            else:
                relation.delete()
                status = 'unfollowed'
            finally:
                fans.following = fans.fans.count()
                fans.save()
                hero.followers = hero.hero.count()
                hero.save()
                json = simplejson.dumps({'error': 0, 'message': status, 'followers': hero.followers})

        return HttpResponse(json)


def following(request, id):
    user = get_object_or_404(User, id=id)
    people =  user.fans.all()
    return render(request, 'user/follow_people.html', {'people': people, 'current': 'following', 'user': user}) 


def followers(request, id):
    user = get_object_or_404(User, id=id)
    people =  user.hero.all()
    return render(request, 'user/follow_people.html', {'people': people, 'current': 'followers', 'user':user })
