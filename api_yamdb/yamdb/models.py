from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(
        max_length = 300,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length = 30,
        verbose_name='Роль',
    )

