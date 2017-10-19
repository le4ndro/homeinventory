from django.conf.urls import url

from . import views
from .views import LocationList, LocationDetail, LocationCreate, LocationUpdate, LocationDelete
from .views import CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete
from .views import ItemList, ItemDetail, ItemCreate, ItemUpdate, ItemDelete

urlpatterns = [
    url(r'^locations/$', LocationList.as_view(), name='location-list'),
    url(r'^locations/(?P<pk>[0-9]+)/$', LocationDetail.as_view(), name='location-detail'),
    url(r'^locations/create$', LocationCreate.as_view(), name='location-create'),
    url(r'^locations/(?P<pk>[0-9]+)/update$', LocationUpdate.as_view(), name='location-update'),
    url(r'^locations/(?P<pk>[0-9]+)/delete$', LocationDelete.as_view(), name='location-delete'),

    url(r'^categoties/$', CategoryList.as_view(), name='category-list'),
    url(r'^categoties/(?P<pk>[0-9]+)/$', CategoryDetail.as_view(), name='category-detail'),
    url(r'^categoties/create$', CategoryCreate.as_view(), name='category-create'),
    url(r'^categoties/(?P<pk>[0-9]+)/update$', CategoryUpdate.as_view(), name='category-update'),
    url(r'^categoties/(?P<pk>[0-9]+)/delete$', CategoryDelete.as_view(), name='category-delete'),

    url(r'^items/$', ItemList.as_view(), name='item-list'),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item-detail'),
    url(r'^items/create$', ItemCreate.as_view(), name='item-create'),
    url(r'^items/(?P<pk>[0-9]+)/update$', ItemUpdate.as_view(), name='item-update'),
    url(r'^items/(?P<pk>[0-9]+)/delete$', ItemDelete.as_view(), name='item-delete'),

    url(r'^register/$', views.register, name='register'),
]
