from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from .models import User


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        exclude = ['first_name', 'last_name', 'password']

    def get_field_names(self, declared_fields, info):
        fields = super(UserSerializer, self).get_field_names(declared_fields, info)
        fields.extend(['get_role_display','is_valid'])
        return fields


class UserPKUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
