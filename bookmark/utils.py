# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup

def get_bookmark_title(url):
    text = urlopen(url).read()
    soup = BeautifulSoup(text)
    return soup.title.string