# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

import HTMLParser

from forms import BookmarkForm
from utils import get_bookmark_title
from ishuqian.models import User
from models import Bookmark, List

def addurl(request):
    if request.method != 'POST':
        return redirect('/')

    url = request.POST.get('url', None)
    title = get_bookmark_title(url.encode('utf-8'))

    form = BookmarkForm(initial={'title':title, 'url': url})
    user = User.objects.get(id = request.session.get('id', None))
    lists = user.list_set.all()
    return render(request, 'bookmark/new.html', {'form': form, 'lists': lists})


def new(request):
    if request.method != 'POST':
        return redirect('/')
    
    user = User.objects.get(id = request.session.get('id', None))

    form = BookmarkForm(request.POST)
    if form.is_valid():
        # lists = request.POST.getlist('lists');
        list = request.POST.get('list', None)
        try:
            l = List.objects.get(id=list)
        except List.DoesNotExist:
            raise Http404

        private = request.POST.get('private', None)
        if private:
            pvalue = 1
        else:
            pvalue = 0

        d = form.save(commit=False)
        d.private = pvalue
        d.user = user
        d.list = l
        d.save()

        #更新list bookmark的数量
        l.bookmarks = Bookmark.objects.filter(user=user, list=list).count()
        l.save()
        return redirect('/home/')

    
    lists = user.list_set.all()
    return render(request, 'bookmark/new.html', {'form': form, 'lists': lists})


@csrf_exempt
def new_list(request):
    if request.method != 'POST':
        raise Http404

    name = request.POST.get('name', None)
    if not name:
        raise Http404

    user = get_object_or_404(User, id=request.session.get('id', None))
    try:
        list = List.objects.get(name=name, user=user)
    except List.DoesNotExist:
        list = List(user=user, name=name)
        list.save()
        json = simplejson.dumps({'error': 0, 'name': list.name, 'value': list.id})
    else:
        json = simplejson.dumps({'error': 1, 'message': u'分类已存在'})

    return HttpResponse(json)