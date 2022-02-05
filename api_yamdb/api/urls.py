from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    GenresViewSet,
    GetConfirmationCodeView,
    GetTokenApiView,
    TitlesViewSet,
    UserViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', GetConfirmationCodeView.as_view()),
    path('v1/auth/token/', GetTokenApiView.as_view()),
    path('v1/', include(router_v1.urls)),
]
