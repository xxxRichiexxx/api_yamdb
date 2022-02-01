from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from.serializers import GetConfirmationCodeSerializer, GetTokenSerializer, UserSerializer


User = get_user_model()

class GetConfirmationCodeView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #генерация пароля
        user, created = User.objects.get_or_create(**serializer.validated_data)
        # user = User.objects.create_user(**serializer.validated_data)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        email = serializer.validated_data['email']
        # отправка письма
        send_mail(
            'Subject here',
            f'Here is the confirmation_code: {password}',
            'andrey@mail.ru',
            [email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



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