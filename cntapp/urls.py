from django.conf.urls import url, patterns, include

from cntapp.views import views, custom


custom_urls = patterns('',
                       url(r'^$', custom.index, name="index"),
                       url(r'^login/$', custom.login_page, name="login"),
                       url(r'^logout/$', custom.logout_admin, name="logout"),
                       url(r'^sys_info/$', custom.sys_info, name="sys_info"),
                       )

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^custom/', include(custom_urls)),
                       )
