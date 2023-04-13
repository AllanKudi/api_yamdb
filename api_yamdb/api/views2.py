from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404

#from .permissions2 import AuthorOrReadOnly, AdminOrReadOnly
from .serializers2 import ReviewSerializer, CommentSerializer
from reviews.models2 import Review


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    #permission_classes = [AuthorOrReadOnly]


    def get_queryset(self):
        """Получить все отзывы к конкретному произведению если оно существует."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews

    def perform_create(self, serializer):
        """Создать отзыв к конкретному произведению если оно существует."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментариев."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    #permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        """Получить все комментарии к конкретному отзыву если он существует."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        """Создать комментарий к конкретному отзыву если он существует."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)