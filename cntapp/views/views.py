from django.shortcuts import render, get_object_or_404

from cntapp.models import Directory


def index(request):
    return render(request, 'cntapp/index.html')


def root(request):
    return directory(request, dir_id=1)  # TODO fix root dir


def directory(request, dir_id):
    d = get_object_or_404(Directory, pk=dir_id)
    return render(request, 'cntapp/dir_list.html', {'dirs': (d.get_sub_dirs())})

