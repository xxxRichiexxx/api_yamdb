from rest_framework import viewsets, mixins, status, permissions
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GetConfirmationCodeSerializer, GetTokenSerializer, UserSerializer
from .permissions import AdminUserModelPermission


User = get_user_model()


class GetConfirmationCodeViewSet(mixins.CreateModelMixin,
                                 viewsets.GenericViewSet):

    serializer_class = GetConfirmationCodeSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        password = User.objects.make_random_password()
        # отправка письма
        send_mail(
            'Subject here',
            f'Here is the confirmation_code: {password}',
            'andrey@mail.ru',
            [email],
            fail_silently=False,
        )
        serializer.save(password=password)


class GetTokenApiView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            access_token = RefreshToken.for_user(user).access_token
            data = {"token": str(access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        errors = {"error": "login or password is incorrect"}
        return Response(errors, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    permission_classes = (AdminUserModelPermission,)

    def get_object(self):
        if self.kwargs['username'] == 'me':
            obj = self.request.user
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()


