from django.http import HttpResponse
from django.shortcuts import render, redirect

from cntapp.models import Directory
from cntapp.helpers import get_root_dirs_names


def index(request):
    if request.method == 'POST':
        Directory.objects.create(name=request.POST['new_dir_name'])
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs})


def first_level(request, first=None):
    if first is not None:
        if first in get_root_dirs_names():
            return HttpResponse("Great, dir found!")
        else:
            return HttpResponse("404")
    else:
        return HttpResponse("hello, some err here?")


def second_level(request, first=None, second=None):
    return HttpResponse("hi")
