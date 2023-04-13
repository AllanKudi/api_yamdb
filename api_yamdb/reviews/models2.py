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
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(choices=SCORE_CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)