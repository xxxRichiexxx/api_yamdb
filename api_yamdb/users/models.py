from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_user

ROLE_CHOICES = (
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class CustomUser(AbstractUser):
    """Кастомная модель пользователей."""
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_user],
        verbose_name='Логин',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Почта',
    )
    bio = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        blank=True,
        default='user',
        verbose_name='Роль',
    )

    class Meta(AbstractUser.Meta):
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
