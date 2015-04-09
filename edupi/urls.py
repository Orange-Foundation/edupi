from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from cntapp.views import views
from edupi import settings


# Backbone's model URL does expect trailing slash
router = DefaultRouter(trailing_slash=False)
router.register(r'directories', views.DirectoryViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('cntapp.urls', namespace='cntapp')),
)

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ) + urlpatterns
