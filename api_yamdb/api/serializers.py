from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import User, Comment, Review


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class GetTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        data['user'] = user
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data


class SignUpSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'me нельзя использовать в качестве имени',
            )
        return value
       
    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Review
    
    def validate_score(self, value):
        """Валидация для поля рейтинг. От 0 до 10."""
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Пожалуйста, укажите значение по 10-ти бальной шкале!'
        )
        return value

    def validate(self, data):
        """Валидация для проверки второго отзыва от одного автора."""
        author = self.context['request'].user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            self.context['request'].method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Нельзя добавить второй отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        #exclude = ('review',)
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    slug = serializers.SlugField(
        max_length=50, min_length=None, allow_blank=False)

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Категория с таким slug уже есть')
        return value

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений."""
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),))

    class Meta:
        model = Title
        fields = '__all__'
