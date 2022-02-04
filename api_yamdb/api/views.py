from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import (Category,
                            Genre,
                            Title)

from .permissions import AdminUserModelPermission, IsAdminOrSuperUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    GetConfirmationCodeSerializer,
    GetTokenSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    UserSerializer
)

User = get_user_model()


class GetConfirmationCodeView(APIView):

    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetTokenApiView(APIView):
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid()
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            access_token = RefreshToken.for_user(user).access_token
            data = {"token": str(access_token)}
            return Response(data, status=status.HTTP_201_CREATED)
        errors = {"error": "password is incorrect"}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


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


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitleGetSerializer
    permission_classes = (IsAdminOrSuperUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostSerializer
        return TitleGetSerializer
