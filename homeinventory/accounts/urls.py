from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^myaccount/$', views.my_account, name='my-account'),
    # url('^change-password/$', auth_views.PasswordChangeView.as_view(),
    #     name='change-password'),
    url('^change-password/$', auth_views.PasswordChangeView.as_view(
        template_name='accounts/change_password.html'),
        name='change-password'),
]
