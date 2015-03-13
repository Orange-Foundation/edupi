from django.conf.urls import url, patterns

from cntapp.views import custom

urlpatterns = patterns('',
                       url(r'^$', custom.index, name="index"),
                       url(r'^(?P<first>.+)/(?P<second>.+)/$', custom.second_level, name="second_level"),
                       url(r'^(?P<first>.+)/$', custom.first_level, name="first_level"),
                       )
