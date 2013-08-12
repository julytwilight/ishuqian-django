# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup

def get_bookmark_title(url):
    try:
        text = urlopen(url).read()
    except IOError:
        return ''
    
    soup = BeautifulSoup(text)
    try:
        return soup.title.string.strip()
    except Exception:
        return ''


def import_bookmarks():
    pass

def current_url(url):
    l = list(url)
    if ''.join(l[:7]) != 'http://':
        if ''.join(l[:8]) != 'https://':
            return 'http://' + url
    return url