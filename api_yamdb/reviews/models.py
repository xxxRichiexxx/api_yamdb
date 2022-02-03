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
        max_length=300,
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=30,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        blank=True,
        default='user'
    )

# extra_kwargs = {'email': {'required': True}}


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug
    pass


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return (
            f'name: {self.name}, '
            f'year: {self.year}, '
            f'description: {self.description}, '
            f'genre: {self.genre}, '
            f'category: {self.category}'
        )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
    pass
