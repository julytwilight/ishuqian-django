# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.http import HttpResponse
def login_required(f):

    def warp(request, *args, **kwargs):
        if not request.session.get('id', None):
            return redirect('/signin/')
        else:
            return f(request, *args, **kwargs)

    return warp