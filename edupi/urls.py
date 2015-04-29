from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from django.contrib import admin

from cntapp.views import views
from edupi import settings


router = DefaultRouter()
router.register(r'directories', views.DirectoryViewSet)
router.register(r'documents', views.DocumentViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
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
