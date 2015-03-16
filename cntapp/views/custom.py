from django.shortcuts import render, render_to_response

from django.template import RequestContext

from cntapp.models import Directory

from cntapp.helpers import get_dir_by_path


def index(request):
    if request.method == 'POST':
        Directory.objects.create(name=request.POST['new_dir_name'])
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs})


def create_dir(request, path):
    if request.method != 'POST':
        return
    d = get_dir_by_path(path)
    if d is not None:
        sub_dir = Directory.objects.create(name=request.POST['new_dir_name'])
        d.add_sub_dir(sub_dir)
    else:
        print('no dir found in path %s!' % path)


def resolve_dirs_structure(request, path):
    if request.method == 'POST':
        create_dir(request, path)
    d = get_dir_by_path(path)
    if d is not None:
        dirs = d.get_sub_dirs()
    else:
        dirs = None
    return render_to_response('cntapp/custom/index.html',
                              {'dirs': dirs},
                              context_instance=RequestContext(request))
