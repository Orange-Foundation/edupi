from django.http import HttpResponse
from django.shortcuts import render, redirect

from cntapp.models import Directory


def index(request):
    if request.method == 'POST':
        Directory.objects.create(name=request.POST['new_dir_name'])
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs})
