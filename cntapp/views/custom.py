from django.shortcuts import render

from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout


def index(request):
    user = request.user
    if user is not None and user.is_superuser and user.is_authenticated():
        return render(request, 'cntapp/custom/index.html')
    else:
        return HttpResponseRedirect(reverse('cntapp:login'))


def login_page(request):
    if request.method != 'POST':
        return render(request, 'cntapp/custom/login.html')

    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('cntapp:index'))
        else:
            # the user is not authenticated with the given username and password
            return HttpResponseRedirect(reverse('cntapp:login'))

    except Exception as e:
        return HttpResponseRedirect(reverse('cntapp:login'))


def logout_admin(request):
    logout(request)
    return HttpResponseRedirect(reverse('cntapp:login'))
