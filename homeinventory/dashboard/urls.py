from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^api/itembycategory$',
        views.total_item_by_category,
        name='total-item-by-category'),
    url(r'^api/itembylocation$',
        views.total_item_by_location,
        name='total-item-by-location'),
]
