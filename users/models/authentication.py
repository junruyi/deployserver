from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

class PrivateToken(Token):

    class Meta:
        verbose_name = _('')