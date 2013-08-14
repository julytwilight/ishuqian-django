# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from bs4 import BeautifulSoup
from time import mktime

from forms import BookmarkForm
from utils import get_bookmark_title, current_url
from ishuqian.models import User
from models import Bookmark, List, Item
from ishuqian.utils import login_required

def addurl(request):
    if request.session.get('id', None) is None:
        request.session['redirect_url'] = request.GET.get('url', None)
        return redirect('signin')

    url   = current_url(request.GET.get('url', None).encode('utf-8'))
    title = get_bookmark_title(url)
    user  = get_object_or_404(User, id=request.session.get('id', None))

    # 添加到Item表
    try:
        item = Item.objects.get(url=url)
        try:
            # 如果书签已存在 直接跳到编辑页面
            bookmark = Bookmark.objects.get(url=item.url, user=user)
            # 如果书签通过导入文件添加 不走item表 所以bookmark表item_id为0
            if bookmark.item_id is None:
                bookmark.item = item
                bookmark.save()
                # 更新item的书签数量
                item.favorites = item.bookmark_set.count()
                item.save()
            return redirect('bookmark_edit', id=bookmark.id)
        except Bookmark.DoesNotExist:
            pass

    except Item.DoesNotExist:
        item = Item(url=url.encode('utf-8'), title=title.encode('utf-8'))
        item.save()
        try:
            # 如果书签已存在 直接跳到编辑页面
            bookmark = Bookmark.objects.get(url=item.url, user=user)
            # 如果书签通过导入文件添加 不走item表 所以bookmark表item_id为0
            if bookmark.item_id is None:
                bookmark.item = item
                bookmark.save()
                # 更新item的书签数量
                item.favorites = item.bookmark_set.count()
                item.save()
            return redirect('bookmark_edit', id=bookmark.id)
        except Bookmark.DoesNotExist:
            pass

    form = BookmarkForm(initial={'title':title})
    lists = user.list_set.all()
    return render(request, 'bookmark/new.html', {'form': form, 'lists': lists, 'item': item})


@login_required
def new(request):
    if request.method != 'POST':
        return redirect('/')
    
    user = get_object_or_404(User, id=request.session.get('id', None))
    item = get_object_or_404(Item, id=request.POST.get('item', None))

    form = BookmarkForm(request.POST)
    if form.is_valid():
        # lists = request.POST.getlist('lists');
        list = request.POST.get('list', None)
        url  = request.POST.get('url', None)

        # 如果文本框和item的url不一致说明用户修改过url 所以跳到404页面
        if item.url != url:
            raise Http404
            # return render(request, 'debug.html', {'debug': [item.url, url]})

        l = get_object_or_404(List, id=list)

        private = request.POST.get('private', None)
        if private:
            pvalue = 1
        else:
            pvalue = 0

        d = form.save(commit=False)
        d.item = item
        d.private = pvalue
        d.user = user
        d.list = l
        d.url = item.url
        d.save()

        #更新有多少用户收藏了这个书签
        item.favorites = item.bookmark_set.exclude(private=1).count()
        item.save()

        #更新list bookmark的数量
        l.bookmarks = Bookmark.objects.filter(user=user, list=list).count()
        l.save()
        user.update_bookmarks()
        return redirect('/home/')
    
    lists = user.list_set.all()
    return render(request, 'bookmark/new.html', {'form': form, 'lists': lists, 'item': item})


@csrf_exempt
@login_required
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


# 编辑书签
@login_required
def edit(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)

    if bookmark.user.id != request.session.get('id', None):
        raise Http404

    if bookmark.item is None:
        try:
            item = Item.objects.get(url=bookmark.url)
        except Exception, e:
            title = get_bookmark_title(bookmark.url)
            item = Item(url=bookmark.url, title=title.encode('utf-8'), favorites=1)
            item.save()
        bookmark.item = item
        bookmark.save()
        item.favorites = item.bookmark_set.count()
        item.save()

    form = BookmarkForm(initial={'title':bookmark.title})

    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            list = get_object_or_404(List, id=request.POST.get('list', None))

            if bookmark.item.url != request.POST.get('url', None) or bookmark.item.id != int(request.POST.get('item', None)):
                raise Http404

            bookmark.title = request.POST.get('title')
            private = request.POST.get('private', None)
            if private:
                pvalue = 1
            else:
                pvalue = 0
            bookmark.private = pvalue
            # 如果修改了分类要更新分类表里的数据
            if bookmark.list != list:
                old_list = bookmark.list
                bookmark.list = list
                bookmark.save()
                old_list.bookmarks = Bookmark.objects.filter(user=bookmark.user, list=old_list).count()
                old_list.save()
                list.bookmarks = Bookmark.objects.filter(user=bookmark.user, list=list).count()
                list.save()
            else:
                bookmark.save()
            
            return redirect('home')

    user = get_object_or_404(User, id=request.session.get('id', None))
    lists = user.list_set.all()
    return render(request, 'bookmark/edit.html', {'form': form, 'lists': lists, 'bookmark': bookmark})


# 删除书签
@login_required
def delete(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)
    bookmark.delete()
    # 更新删除书签分类数量
    bookmark.list.bookmarks = bookmark.list.bookmark_set.count()
    bookmark.list.save()
    # 更新用户书签数量
    user = get_object_or_404(User, id=request.session.get('id', None))
    user.update_bookmarks()

    return redirect(request.META.get('HTTP_REFERER', None))


# 分类列表
@login_required
def list_index(request):
    lists = get_object_or_404(User, id=request.session.get('id', None)).list_set.exclude(name=u'默认分类')
    return render(request, 'bookmark/list.html', {'lists': lists})


# 更新分类名称
@login_required
def list_update(request, id):
    if request.method != 'POST' or not request.POST.get('name', None):
        raise Http404

    list = List.objects.get(id=id, user_id=request.session.get('id', None))
    list.name = request.POST.get('name', None)
    list.save()

    return redirect('list')


# 列表删除
@login_required
def list_delete(request, id):
    list = List.objects.get(id=id, user_id=request.session.get('id', None))
    default = List.objects.get(user_id=request.session.get('id', None), name=u'默认分类')
    list.bookmark_set.all().update(list=default)
    list.delete()
    default.bookmarks = default.bookmark_set.count()
    default.save()
    return redirect('list')


# 删除列表及书签
@login_required
def list_delall(request, id):
    list = List.objects.get(id=id, user_id=request.session.get('id', None))
    list.bookmark_set.all().delete()
    list.delete()
    user = get_object_or_404(User, id=request.session.get('id', None))
    user.update_bookmarks()
    return redirect('list')


# 更新书签到列表
@login_required
def bookmarks_change(request):
    bs = request.POST.getlist('bm_box');
    id = request.POST.get('id', None)
    l = get_object_or_404(List, id=id)
    bookmarks = Bookmark.objects.filter(id__in=bs)
    lids = [b.list_id for b in bookmarks]
    lids.append(int(id))
    lids = set(lids)
    bookmarks.update(list=l)
    for l in lids:
        lt = get_object_or_404(List, id=l)
        lt.bookmarks = lt.bookmark_set.count()
        lt.save()
    return redirect(request.META.get('HTTP_REFERER', None))


# 删除多个书签
@login_required
def bookmarks_delete(request):
    bs = request.POST.getlist('bm_box');
    bookmarks = Bookmark.objects.filter(id__in=bs)
    lids = [b.list_id for b in bookmarks]
    lids = set(lids)
    bookmarks.delete()
    for l in lids:
        lt = get_object_or_404(List, id=l)
        lt.bookmarks = lt.bookmark_set.count()
        lt.save()

    # 把user bookmarks数量写成函数
    user = get_object_or_404(User, id=request.session.get('id', None))
    user.update_bookmarks()
    return redirect(request.META.get('HTTP_REFERER', None))


# 导入书签
@login_required
def bookmarks_import(request):
    user = get_object_or_404(User, id=request.session.get('id', None))
    list = List.objects.get(name=u'默认分类', user=user)
    if request.method == 'POST':
        bf = request.FILES['file']
        text = ''
        for t in bf.chunks():
            text += t

        soup = BeautifulSoup(text)
        try:
            links = soup.dl.find_all('a')
        except Exception, e:
            return HttpResponse('请导入正确的书签文件')
            
        for l in links:
            url = l.get('href').encode('utf-8')
            try:
                title = l.string.encode('utf-8')
            except Exception:
                title = url
            # bookmark是否存在
            try:
                bookmark = Bookmark.objects.get(url=url, user_id=request.session.get('id', None))
            except Bookmark.DoesNotExist:
                Bookmark.objects.create(user=user, private=0, list=list, url=url, title=title)

        list.bookmarks = list.bookmark_set.count()
        list.save()
        user.update_bookmarks()
        return redirect('home_list', id=list.id)

    return render(request, 'bookmark/import.html')


# 导出书签
@login_required
def bookmarks_export(request):
    user = get_object_or_404(User, id=request.session.get('id', None))
    bookmarks = user.bookmark_set.order_by('list')
    html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
<DT><H3 ADD_DATE="1362544437" PERSONAL_TOOLBAR_FOLDER="true">ishuqian</H3>
<DL><p>
"""
    start = '<DL><p>'
    end   = '</DL><p>'
    current_list = 0
    for b in bookmarks:
        if b.list_id != current_list:
            if current_list != 0:
                html += '\t'
                html += end
                html += '\n'
            html += '\t<DT><H3 ADD_DATE="%d">%s</H3>\n\t\t%s\n' % (int(mktime(b.addtime.timetuple())), b.list.name, start)
            current_list = b.list_id
        html += '\t\t\t<DT><A HREF="%s" ADD_DATE="">%s</A>\n' % (b.url, b.title)
    html += '''\t\t</DL><p>
</DL><p>
</DL><p>
'''
    response = HttpResponse(mimetype="application/octet-stream")
    response["Content-Disposition"] = "attachment; filename=IshuqianBookmarks.html"
    response.write(html)
    return response


# 打开item
def item(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'bookmark/item.html', {'item': item})


# item评论
def item_reply(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'bookmark/reply.html', {'item': item})
# 通过bookmark获取item
def bookmark_reply(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)
    if bookmark.item is None:
        try:
            item = Item.objects.get(url=bookmark.url)
        except Item.DoesNotExist:
            item = Item(title=get_bookmark_title(bookmark.url), url=bookmark.url, favorites=1)
            item.save()
        bookmark.item = item
        bookmark.save()
        item.favorites = item.bookmark_set.count()
        item.save()
    else:
        item = bookmark.item

    return redirect('item_reply', id=item.id)


# go_to 页面跳转
def bookmark_go(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)
    return redirect(bookmark.url)
def item_go(request, id):
    item = get_object_or_404(Item, id=id)
    return redirect(item.url)
