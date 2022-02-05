from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведений."""
    name = models.TextField(verbose_name='Название')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True, verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'name: {self.name}, '
            f'year: {self.year}, '
        )


class GenreTitle(models.Model):
    """Модель для связи произведений и жанров отношением многие ко многим."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre}  ---  {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='текст',
    )
    author = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'

    def __str__(self):
        return self.text[:60]


class Comment(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
