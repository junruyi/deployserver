from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core import signing
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import reverse


class User(AbstractUser):
    ROLE_CHOICES=(
        ('Admin',_('Administrator')),
        ('Manager',_('Porject manager')),
        ('Dev',_('Development'))
    )
    username = models.CharField(max_length=20, unique=True, verbose_name=_('Username'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    email = models.EmailField(max_length=30, unique=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone'))
    role = models.CharField(choices=ROLE_CHOICES, default='Dev', max_length=10, blank=True,verbose_name=_('Role'))
    class Meta:
        permissions = (
            ('view_user', 'can view user'),
        )

    def get_absolute_url(self):
        return reverse('users:user-detail', args=(self.id,))

    @property
    def password_raw(self):
       raise AttributeError('Password raw is not a readable attribute')

    @password_raw.setter
    def password_raw(self,password_raw_):
        self.set_password(password_raw_)

    @property
    def is_valid(self):
        if self.is_active:
            return True
        return False

    @property
    def is_superuser(self):
        if self.role == 'Admin':
            return True
        return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'Dev'

    @property
    def is_dev(self):
        return self.role == 'Dev'

    @property
    def is_manager(self):
        return self.role == 'Manager'

    @property
    def is_staff(self):
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        super(User, self).save(*args,**kwargs)

    def delete(self):
        if self.role == 'Admin':
            return super(User,self).delete()

    @classmethod
    def init_account(cls):
        user = cls(username = 'admin',
                   email= 'admin@junruyi.cc',
                   name=_('Administrator'),
                   role='Admin',
                   phone='13000000000',
                   password_raw='mtjyy123'
                   )
        user.save()