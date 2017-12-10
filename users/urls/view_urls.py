from __future__ import absolute_import

from django.conf.urls import url
from users import views

app_name = 'users'

urlpatterns = [
    url(r'^login$', views.UserLoginView.as_view(), name='login'),
]