from django.db import models


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
        ordering = ('Имя',)

    def __str__(self):
        return self.name

