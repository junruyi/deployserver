from __future__ import absolute_import

from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^login$', views.UserLoginView.as_view(), name='login')
]