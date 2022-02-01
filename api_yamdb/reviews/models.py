from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField(max_length=16, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=16)
    slug = models.SlugField(max_length=16, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=16)
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre, through='GenreTitle'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return (
            f'name: {self.name}, '
            f'year: {self.year}, '
            f'genre: {self.genre}, '
            f'category: {self.category}'
        )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
