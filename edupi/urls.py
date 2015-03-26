from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from cntapp.views import views


router = DefaultRouter()
router.register(r'directories', views.DirectoryViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('cntapp.urls', namespace='cntapp')),
)
