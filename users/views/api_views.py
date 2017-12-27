from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_bulk import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .. import serializers
from ..models import User
from ..utils import check_user_valid, generate_token
from ..permissions import IsSuperUser, IsValidUser, IsCurrentUserOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsSuperUser,)
    filter_fields = ('username', 'email', 'name', 'id')


class UserResetPasswordApi(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def perform_update(self, serializer):
        import uuid
        from ..utils import send_reset_password_mail

        user = self.get_object()
        user.password_raw = str(uuid.uuid4())
        user.save()
        send_reset_password_mail(user)


class UserToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        if not request.user.is_authenticated:
            username = request.data.get('username', '')
            email = request.data.get('email', '')
            password = request.data.get('password', '')

            user, msg = check_user_valid(username=username, email=email,
                                         password=password)

        if user:
            token = generate_token(request, user)
            return Response({'Token': token, 'Keyword': 'Bearer'}, status=200)
        else:
            return Response({'error': msg}, status=406)


class UserProfile(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request):
        return Response(request.user.to_json())

    def post(self, request):
        return Response(request.user.to_json())


class UserAuthApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        login_type = request.data.get('login_type', '')
        login_ip = request.data.get('remote_addr', None)
        user_agent = request.data.get('HTTP_USER_AGENT', '')

        user, msg = check_user_valid(username=username, password=password)

        if user:
            token = generate_token(request, user)
            return Response({'token': token, 'user': user.to_json()})
        else:
            return Response({'msg': msg}, status=401)




