from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from user.models import User, Review
from api.permissions3 import AdminOnly, AllPermission
from api.serializers3 import (GetTokenSerializer, SignUpSerializer,
                              UsersSerializer, ReviewSerializer,
                              CommentSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код доступа',
            message=f'Код доступа {confirmation_code}',
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny, ])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = AccessToken.for_user(serializer.data.user)
    return Response({'token': str(token)},
                    status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly, )
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('=username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [AllPermission,]


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
    permission_classes = [AllPermission,]

    def get_queryset(self):
        """Получить все комментарии к конкретному отзыву если он существует."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments

    def perform_create(self, serializer):
        """Создать комментарий к конкретному отзыву если он существует."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
