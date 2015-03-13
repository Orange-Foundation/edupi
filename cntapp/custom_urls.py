from django.conf.urls import url, patterns

from cntapp.views import custom

urlpatterns = patterns('',
                       url(r'^$', custom.index, name="index"),
                       url(r'^(?P<urls>[\w/]*)/$', custom.resolve_dirs_structure, name="resolve_dirs_structure"),
                       )
