from django.urls import path

from .views import GetConfirmationCodeViewSet #GetTokenViewSet


urlpatterns = [
    path('v1/auth/signup/', GetConfirmationCodeViewSet.as_view({'post': 'create'})),
    # path('v1/auth/token/', GetTokenViewSet.as_view()),
]
