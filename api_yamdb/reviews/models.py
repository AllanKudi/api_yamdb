from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

#from api.serializers import SignUpSerializer


SCORE_CHOICES = (
         (1, 'Ужасно'),
         (2, 'Плохо'),
         (3, 'Удовлетворительно'),
         (4, 'Сносно'),
         (5, 'Средне'),
         (6, 'Хорошо'),
         (7, 'Отлично'),
         (8, 'Прекрасно'),
         (9, 'Супер'),
         (10, 'Превосходно'),
     )


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        #validators=(SignUpSerializer, UnicodeUsernameValidator),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=100,
        choices=ROLE,
        default=USER,
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff


class Review(models.Model):
    """Модель отзывов к произведениям."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='Произведение, к которому пойдет отзыв',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Напишите текст вашего отзыва!',
    )
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления отзыва', 
        auto_now_add=True, db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )]
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв, к которому пойдет комментарий',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите текст вашего комментария!',
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True, db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return self.text