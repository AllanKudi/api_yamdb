from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models2 import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
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
        if 0 > value > 10:
            raise serializers.ValidationError('Пожалуйста, укажите значение по 10-ти бальной шкале!')
        return value

    def validate(self, data):
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
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
