import logging
from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User

csv_files = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv')
)


class Command(BaseCommand):
    help = ('Загрузка данных из reviews/static/data/*.csv.'
            'Запуск: python manage.py baseimport.'
            'Подробнее об импорте в README.md.')

    def handle(self, *args, **options):
        logging.info('Начинаем загрузку данных.')
        for model, csv in csv_files:
            with open(f'./static/data/{csv}', encoding='utf-8') as file:
                if model.objects.exists():
                    logging.info(f'{model.__name__} Данные загружены.')
                    continue
                reader = DictReader(file)
                model.objects.bulk_create(model(**data) for data in reader)
            logging.info('Поздравляем! Все данные загружены.')
