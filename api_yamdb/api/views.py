from rest_framework import viewsets
from rest_framework import mixins
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from.serializers import GetConfirmationCodeSerializer


User = get_user_model()

class GetConfirmationCodeViewSet(
    mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = GetConfirmationCodeSerializer

    def perform_create(self, serializer):
        #генерация пароля
        password = User.objects.make_random_password()
        # отправка письма
        send_mail(
            'Subject here',
            f"Here is the message. {password}",
            'andrey@mail.ru',
            ['andrey@yandex.ru'],
            fail_silently=False,
        )
        serializer.save(password=password)
