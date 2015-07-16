from django.conf.urls import url, patterns, include

from cntapp.views import views, custom, stats


custom_urls = patterns('',
                       url(r'^$', custom.index, name="index"),
                       url(r'^login/$', custom.login_page, name="login"),
                       url(r'^logout/$', custom.logout_admin, name="logout"),
                       url(r'^sys_info/$', custom.sys_info, name="sys_info"),

                       url(r'^documents_stats/$', stats.documents_stats, name="documents_stats"),
                       url(r'^stats/status/$', stats.get_stats_status, name="get_stats_status"),
                       url(r'^stats/start/$', stats.start_stats, name="start_stats"),
                       url(r'^stats/$', stats.stats, name="stats"),
                       )

urlpatterns = patterns('',
                       url(r'^$', views.index, name="index"),
                       url(r'^custom/', include(custom_urls)),
                       )
