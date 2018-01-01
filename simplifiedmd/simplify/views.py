# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.http import JsonResponse
from summarizer import core
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import json

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

def typeahead(request):
    title = request.POST.get('title', None)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_data = open(BASE_DIR + '/summarized_db.json').read()
    result = []
    for row in json.loads(json_data):
        row_title = row[1]
        if (row_title.lower().find(title.lower()) != -1):
            result.append(row_title)
    return JsonResponse({'results': result})

def lookup(request):
    title = request.POST.get('title', None)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_data = open(BASE_DIR + '/summarized_db.json').read()
    text = ''
    for row in json.loads(json_data):
        row_title = row[1]
        if (row_title == title):
            text = row[2]
    data = {
        'simplified_text': text
    }
    return JsonResponse(data)
