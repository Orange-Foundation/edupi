from django.conf.urls import url, patterns, include

from cntapp.views import views, custom


custom_urls = patterns('',
                       url(r'^$', custom.index, name="index"),
                       )

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^dirs/$', views.root, name="root"),
                       url(r'^dirs/(?P<dir_id>\d+)/$', views.directory, name="directory"),
                       url(r'^custom/', include(custom_urls)),
                       )
