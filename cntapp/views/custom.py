from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext

from cntapp.models import Directory
from cntapp.helpers import get_root_dirs_names, get_root_dirs, get_dir_by_path


def index(request):
    if request.method == 'POST':
        Directory.objects.create(name=request.POST['new_dir_name'])
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs})


def resolve_dirs_structure(request, path):
    path = str(path)
    d = get_dir_by_path(path)
    if d is not None:
        dirs = d.get_sub_dirs()
    else:
        dirs = None
    return render_to_response('cntapp/custom/index.html',
                              {'dirs': dirs},
                              context_instance=RequestContext(request))
