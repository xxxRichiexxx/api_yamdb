from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GetConfirmationCodeView, GetTokenApiView, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', GetConfirmationCodeView.as_view()),
    path('v1/auth/token/', GetTokenApiView.as_view()),
    path('v1/', include(router.urls)),
]
