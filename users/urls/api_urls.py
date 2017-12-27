from __future__ import absolute_import

from django.conf.urls import url
from rest_framework_bulk.routes import BulkRouter
from users import views

app_name = 'users'

router = BulkRouter()
router.register(r'v1/users', views.UserViewSet, 'user')

urlpatterns = [
    url(r'^v1/token/$', views.UserToken.as_view(), name='user-token'),
    url(r'^v1/profile/$', views.UserProfile.as_view(), name='user-profile'),
    url(r'v1/auth/$', views.UserAuthApi.as_view(), name='user-auth'),
    url(r'^v1/usrs/(?P<pk>\d+)/password/reset/$',
        views.UserResetPasswordApi.as_view(), name='user-reset-password'),
]

urlpatterns += router.urls