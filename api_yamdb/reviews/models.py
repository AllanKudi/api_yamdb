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
    validators=(UnicodeUsernameValidator,), #SignUpSerializer, ),
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


class AbstractNameModel(models.Model):
    """Абстрактная модель name + slug."""

    slug = models.SlugField(
        'Slug',
        max_length=250,
        unique=True,
    )
    name = models.CharField(
        'Название',
        max_length=250,
    )

    class Meta:
        abstract = True
        ordering = ('name', )

    def __str__(self):
        return self.name


class Category(AbstractNameModel):
    """Модель типа произведения"""

    class Meta(AbstractNameModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genre(AbstractNameModel):
    """Модель жанра произведений."""

    class Meta(AbstractNameModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = 'genres'


class Title(models.Model):
    """Модель произведения."""

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='titles',
    )
    description = models.TextField(
        'Описание',
        db_index=True,
        max_length=250,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    name = models.CharField(
        'Название',
        max_length=250,
        db_index=True,
    )
    year = models.IntegerField(
        'Год выпуска',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'  

    def __str__(self):
        return self.name


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
