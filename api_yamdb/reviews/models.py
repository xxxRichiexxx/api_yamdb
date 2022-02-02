from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_user

ROLE_CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        unique=True,
        validators=[validate_user]
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    bio = models.CharField(
        max_length = 300,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length = 30,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
    )

# extra_kwargs = {'email': {'required': True}}


