import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, GenreTitle, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = options['filename'][0]
        with open('C:/Dev/api_yamdb/api_yamdb/static/data/{}'.format(filename), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            if filename == 'category.csv':
                for row in reader:
                    _, created = Category.objects.get_or_create(
                        name=row[1],
                        slug=row[2],
                    )
            elif filename == 'genre.csv':
                for row in reader:
                    _, created = Genre.objects.get_or_create(
                        name=row[1],
                        slug=row[2],
                    )
            elif filename == 'titles.csv':
                for row in reader:
                    _, created = Title.objects.get_or_create(
                        name=row[1],
                        year=row[2],
                        category_id=row[3],
                    )
            elif filename == 'genre_title.csv':
                for row in reader:
                    _, created = GenreTitle.objects.get_or_create(
                        genre_id=row[2],
                        title_id=row[1],
                    )

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs=1,
            type=str
        )
