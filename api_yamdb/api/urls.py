from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    GetConfirmationCodeView,
    GetTokenApiView,
    TitlesViewSet,
    UserViewSet
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', GetConfirmationCodeView.as_view()),
    path('v1/auth/token/', GetTokenApiView.as_view()),
    path('v1/', include(router_v1.urls)),
]
