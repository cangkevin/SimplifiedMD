# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.http import JsonResponse
from summarizer import core

@ensure_csrf_cookie
def index(request):
    return render(request, 'simplify/home.html')
    
def simplify_text(request):
    text = request.POST.get('text', None)
    length = int(request.POST.get('length', None))
    text = core.summarize(text, length)
    data = {
        'simplified_text': text
    }
    return JsonResponse(data)
