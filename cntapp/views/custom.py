from django.shortcuts import render, render_to_response

from django.template import RequestContext

from cntapp.models import Directory

from cntapp.helpers import get_dir_by_path
from cntapp.forms import DirectoryForm


def index(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            Directory.objects.create(name=form.cleaned_data['name'])
        else:
            pass  # TODO
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs, 'form': DirectoryForm()})


def create_dir(request, path):
    if request.method != 'POST':
        return
    form = DirectoryForm(request.POST)
    d = get_dir_by_path(path)
    if d is not None and form.is_valid():
        sub_dir = Directory.objects.create(name=form.cleaned_data['name'])
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
                              {'dirs': dirs, 'form': DirectoryForm()},
                              context_instance=RequestContext(request))
