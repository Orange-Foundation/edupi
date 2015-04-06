from django.shortcuts import render

from cntapp.models import Directory


def index(request):
    dirs = [d for d in (Directory.objects.all()) if d.get_parents().count() == 0]
    return render(request, 'cntapp/custom/index.html', {'dirs': dirs})
