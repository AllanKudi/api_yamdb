from django.db import models


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