from django.conf.urls import url

from . import views
from .views import LocationList, LocationDetail, LocationCreate, LocationUpdate, LocationDelete

urlpatterns = [
    url(r'^locations/$', LocationList.as_view(), name='location-list'),
    url(r'^locations/(?P<pk>[0-9]+)/$', LocationDetail.as_view(), name='location-detail'),
    url(r'^locations/create$', LocationCreate.as_view(), name='location-create'),
    url(r'^locations/(?P<pk>[0-9]+)/update$', LocationUpdate.as_view(), name='location-update'),
    url(r'^locations/(?P<pk>[0-9]+)/delete$', LocationDelete.as_view(), name='location-delete'),
    url(r'^register/$', views.register, name='register'),
]
