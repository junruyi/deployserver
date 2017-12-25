from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.authentication import CSRFCheck
from .models import User, PrivateToken


class PrivateTokenAuthentication(authentication.TokenAuthentication):
    model = PrivateToken


class SessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        reason = CSRFCheck().process_view(request, None, (), {})
        if reason:
            raise exceptions.AuthenticationFailed(reason)


