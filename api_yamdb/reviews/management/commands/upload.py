import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, GenreTitle, Title, Comment, Review

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs=1,
            type=str
        )

    def handle(self, *args, **options):
        filename = options['filename'][0]
        path = os.path.join(settings.BASE_DIR, "static/data/") + filename
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            if filename == 'category.csv':
                for row in reader:
                    _, created = Category.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
            elif filename == 'genre.csv':
                for row in reader:
                    _, created = Genre.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2],
                    )
            elif filename == 'titles.csv':
                for row in reader:
                    _, created = Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category_id=row[3],
                    )
            elif filename == 'genre_title.csv':
                for row in reader:
                    _, created = GenreTitle.objects.get_or_create(
                        id=row[0],
                        genre_id=row[2],
                        title_id=row[1],
                    )
            elif filename == 'users.csv':
                for row in reader:
                    _, created = User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6],
                    )
            elif filename == 'review.csv':
                for row in reader:
                    _, created = Review.objects.get_or_create(
                        id=row[0],
                        title_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        score=row[4],
                        pub_date=row[5]
                    )
            elif filename == 'comments.csv':
                for row in reader:
                    _, created = Comment.objects.get_or_create(
                        id=row[0],
                        review_id=row[1],
                        text=row[2],
                        author_id=row[3],
                        pub_date=row[4],
                    )
