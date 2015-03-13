from django.conf.urls import url, patterns

from cntapp.views import custom

urlpatterns = patterns('',
                       url(r'^$', custom.index, name="index"),
                       )
