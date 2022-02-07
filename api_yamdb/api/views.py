from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Category,
    Genre,
    Title,
    Review
)
from .permissions import (
    AdminPermission,
    ForMePermission,
    ReadOnlyPermission,
    CreateAndUpdatePermission,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    GetConfirmationCodeSerializer,
    GetTokenSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer
)
from django.conf import settings
from .my_filters import TitlesFilter

User = get_user_model()


class GetConfirmationCodeView(APIView):
    """
    При получении POST-запроса с параметрами email и username
    отправляет письмо с кодом подтверждения (confirmation_code)
    на указанный адрес email.
    """
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        to_email = serializer.validated_data['email']
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'You have registered with the Reviews service',
            f'This is the confirmation code: {confirmation_code}',
            settings.FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetTokenApiView(APIView):
    """
    При получении POST-запроса с параметрами username
    и confirmation_code возвращает JWT-токен.
    """
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            access_token = RefreshToken.for_user(user).access_token
            data = {"token": str(access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        errors = {"error": "confirmation code is incorrect"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Реализует основные операции с моделью пользователей:
    - получения списка пользователей
    - создание пользователя
    - получение детализации по пользователю
    - редактирование поьзователя
    - удаление пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    permission_classes = (AdminPermission | ForMePermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('role', 'is_superuser', )
    search_fields = ('username', 'email', 'role', 'bio', )

    def get_object(self):
        if self.kwargs['username'] == 'me':
            obj = self.request.user
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CategoriesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Реализует основные операции с моделью категорий:
    - получения списка категорий
    - создание категории
    - удаление категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission | ReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class GenresViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Реализует основные операции с моделью жанров:
    - получения списка жанров
    - создание жанра
    - удаление жанра.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission | ReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Реализует основные операции с моделью произведений:
    - возвращает список всех произведений
    - добавление нового произведения
    - возвращает информацию о произведении
    - обновляет информацию о произведении
    - удаляет произведение
    """
    queryset = Title.objects.all()
    permission_classes = (AdminPermission | ReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminPermission
                          | ReadOnlyPermission
                          | CreateAndUpdatePermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AdminPermission
                          | ReadOnlyPermission
                          | CreateAndUpdatePermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
