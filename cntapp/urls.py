from django.conf.urls import url, patterns

from cntapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^dirs/$', views.root, name="root"),
                       url(r'^dirs/(?P<dir_id>\d+)/$', views.directory, name="directory"),
)
