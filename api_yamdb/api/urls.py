from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GetConfirmationCodeViewSet, GetTokenApiView, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', GetConfirmationCodeViewSet.as_view({'post': 'create'})),
    path('v1/auth/token/', GetTokenApiView.as_view()),
    path('v1/', include(router.urls)),
]
