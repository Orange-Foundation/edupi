from django.conf.urls import patterns, include, url

from edupi.admin_site import cms_site


urlpatterns = patterns(
    '',
    url(r'^', include('cntapp.urls', namespace='cntapp'))
)
