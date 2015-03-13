from django.shortcuts import render, get_object_or_404

from cntapp.models import Directory


def index(request):
    return render(request, 'cntapp/index.html')


def root(request):
    return directory(request)


def directory(request, dir_id=None):
    if dir_id is None:
        dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    else:
        d = get_object_or_404(Directory, pk=dir_id)
        dirs = d.get_sub_dirs()

    return render(request, 'cntapp/dir_list.html', {'dirs': dirs})



