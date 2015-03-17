from django.conf.urls import url, patterns, include

from cntapp.views import views, custom


custom_urls = patterns('',
                       url(r'^$', custom.index, name="index"),
                       url(r'^(?P<path>[\w/]*)/$', custom.resolve_dirs_structure, name="resolve_dirs_structure"),
                       )

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^dirs/$', views.root, name="root"),
                       url(r'^dirs/(?P<dir_id>\d+)/$', views.directory, name="directory"),
                       url(r'^custom/', include(custom_urls)),
                       )
