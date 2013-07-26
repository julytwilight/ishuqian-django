# -*- coding: utf-8 -*-
from django import forms

from models import Bookmark, List
from ishuqian.models import User

class BookmarkForm(forms.ModelForm):

    class Meta():
        model = Bookmark
        fields = ('url', 'title')
        widgets = {
            'url': forms.TextInput(attrs={'class':'input'}),
            'title': forms.TextInput(attrs={'class':'input'}),
        }