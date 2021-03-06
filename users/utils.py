from collections import  OrderedDict
from six import  string_types
import  os
import base64
import uuid
from itertools import chain
import string
import logging

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.shortcuts import reverse

from .models import User
from common.task import send_mail_async
from common.utils import get_object_or_none

logger = logging.getLogger('deployserver')


class AdminUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True



def user_add_success_next(user):
    subject = _('Create account successfully')
    recipient_list = [user.email]
    message = _("""
    Hello %(name)s:
    </br>
    Your account has been created successfully
    </br>
    <a href="%(rest_password_url)s?token=%(rest_password_token)s">click here to set your password</a>
    </br>
    This link is valid for 1 hour. After it expires, <a href="%(forget_password_url)s?email=%(email)s">request new one</a>

    </br>
    ---

    </br>
    <a href="%(login_url)s">Login direct</a>

    </br>
    """) % {
        'name': user.name,
        'rest_password_url': reverse('users:reset-password', external=True),
        'rest_password_token': user.generate_reset_token(),
        'forget_password_url': reverse('users:forgot-password', external=True),
        'email': user.email,
        'login_url': reverse('users:login', external=True),
    }

    send_mail_async.delay(subject, message, recipient_list, html_message=message)


def send_reset_password_mail(user):
    subject = _('Reset password')
    recipient_list = [user.email]
    message = _("""
    Hello %(name)s:
    </br>
    Please click the link below to reset your password, if not your request, concern your account security
    </br>
    <a href="%(rest_password_url)s?token=%(rest_password_token)s">Click here reset password</a>
    </br>
    This link is valid for 1 hour. After it expires, <a href="%(forget_password_url)s?email=%(email)s">request new one</a>

    </br>
    ---

    </br>
    <a href="%(login_url)s">Login direct</a>

    </br>
    """) % {
        'name': user.name,
        'rest_password_url': reverse('users:reset-password', external=True),
        'rest_password_token': user.generate_reset_token(),
        'forget_password_url': reverse('users:forgot-password', external=True),
        'email': user.email,
        'login_url': reverse('users:login', external=True),
    }
    if settings.DEBUG:
        logger.debug(message)

    send_mail_async.delay(subject, message, recipient_list, html_message=message)


def check_user_valid(kwargs: object) -> object:
    username = kwargs.pop('username', None)
    password = kwargs.pop('password', None)
    email = kwargs.pop('email', None)

    if username:
        user = get_object_or_none(User, username=username)
    elif email:
        user = get_object_or_none(User, email=email)
    else:
        user = None

    if user is None:
        return None, _('User not exist')
    elif not user.is_valid:
        return None, _('Disabled or expired')

    if password and authenticate(username=username, password=password):
        return user, ''

    return None, _('Password or SSH public key invalid')


def generate_token(request, user):
    expiration = settings.CONFIG.TOKEN_EXPIRATION or 3600
    remote_addr = request.META.get('X_HTTP_REAL_IP') or \
          request.META.get('REMOTE_ADDR', '')

    if not isinstance(remote_addr, bytes):
        remote_addr = remote_addr.encode('utf-8')
    remote_addr = base64.b16decode(remote_addr)
    token = cache.get('%s_%s' % (user.id, remote_addr))
    if not token:
        token = uuid.uuid4().hex
        print('Set cache: %s' % token)
        cache.set(token, user.id, expiration)
        cache.set('%s_%s' % (user.id, remote_addr), token, expiration)
    return token