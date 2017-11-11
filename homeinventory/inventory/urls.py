from django.conf.urls import url

from homeinventory.inventory import views
from homeinventory.inventory.views import LocationList, LocationDetail
from homeinventory.inventory.views import LocationCreate
from homeinventory.inventory.views import LocationUpdate, LocationDelete
from homeinventory.inventory.views import CategoryList, CategoryDetail
from homeinventory.inventory.views import CategoryCreate
from homeinventory.inventory.views import CategoryUpdate, CategoryDelete
from homeinventory.inventory.views import ItemList, ItemDetail, ItemCreate
from homeinventory.inventory.views import ItemUpdate, item_loan_returned
from homeinventory.inventory.views import ItemDelete, ItemAttachmentView
from homeinventory.inventory.views import ItemPhotoView, ItemLoanCreate

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^locations/$', LocationList.as_view(), name='location-list'),
    url(r'^locations/(?P<pk>[0-9]+)/$',
        LocationDetail.as_view(), name='location-detail'),
    url(r'^locations/create$',
        LocationCreate.as_view(),
        name='location-create'),
    url(r'^locations/(?P<pk>[0-9]+)/update$',
        LocationUpdate.as_view(),
        name='location-update'),
    url(r'^locations/(?P<pk>[0-9]+)/delete$',
        LocationDelete.as_view(),
        name='location-delete'),

    url(r'^categoties/$', CategoryList.as_view(), name='category-list'),
    url(r'^categoties/(?P<pk>[0-9]+)/$',
        CategoryDetail.as_view(),
        name='category-detail'),
    url(r'^categoties/create$',
        CategoryCreate.as_view(),
        name='category-create'),
    url(r'^categoties/(?P<pk>[0-9]+)/update$',
        CategoryUpdate.as_view(),
        name='category-update'),
    url(r'^categoties/(?P<pk>[0-9]+)/delete$',
        CategoryDelete.as_view(),
        name='category-delete'),

    url(r'^items/$', ItemList.as_view(), name='item-list'),
    url(r'^items/(?P<pk>[0-9]+)/$', ItemDetail.as_view(), name='item-detail'),
    url(r'^items/create$', ItemCreate.as_view(), name='item-create'),
    url(r'^items/(?P<pk>[0-9]+)/update$',
        ItemUpdate.as_view(),
        name='item-update'),
    url(r'^items/(?P<pk>[0-9]+)/delete$',
        ItemDelete.as_view(),
        name='item-delete'),

    url(r'^items/(?P<pk>[0-9]+)/attachments$',
        ItemAttachmentView.as_view(),
        name='item-attachment'),

    url(r'^items/(?P<pk>[0-9]+)/photos$',
        ItemPhotoView.as_view(),
        name='item-photo'),

    url(r'^itemattachments/(?P<pk>[0-9]+)/remove$',
        views.item_attachment_delete,
        name='attachment-remove'),

    url(r'^itemphotos/(?P<pk>[0-9]+)/remove$',
        views.item_photo_delete,
        name='photo-remove'),

    url(r'^items/(?P<pk>[0-9]+)/loans$',
        ItemLoanCreate.as_view(),
        name='item-loan-create'),

    url(r'^items/(?P<pk>[0-9]+)/returned$',
        views.item_loan_returned,
        name='item-loan-returned'),

    url(r'^register/$', views.register, name='register'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
