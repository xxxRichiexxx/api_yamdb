import datetime as dt

from rest_framework import serializers
from django.db.models import Q, Avg
from django.contrib.auth import get_user_model

from users.validators import validate_user
from reviews.models import (Category,
                            Genre,
                            Title,
                            Comment,
                            Review,
                            )

User = get_user_model()


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
    """
    Проверяет username и email перед выдачей confirmation_code
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validate_user]
    )
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate(self, data):
        if User.objects.filter(~Q(email=data['email']),
                               username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует!')
        elif User.objects.filter(~Q(username=data['username']),
                                 email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!')
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        return user


class GetTokenSerializer(serializers.Serializer):
    """
    Проверяет username и confirmation_code перед выдачей токена
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализует/десериализует данные модели User.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_role(self, value):
        """Запрещаем поьзователю менять свою роль на admin"""
        user = self.context['request'].user
        if user.role == 'user' and value == 'admin':
            value = 'user'
        return value


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализует/десериализует данные модели Category.
    """
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализует/десериализует данные модели Genre.
    """
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    """
    Сериализует данные модели Title.
    """
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        """Вычисляем средний рейтинг для произведения."""
        return obj.reviews.aggregate(Avg("score"))['score__avg']


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Десериализует данные для модели Title.
    """
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {'description': {'required': False}}

    def validate_year(self, value):
        """Год выпуска произведения не может быть больше текущего."""
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска превышает текущий!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализует/десериализует данные модели Review.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='pk',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        """Можно оставить только один отзыв."""
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if (self.context['request'].method != 'PATCH'
                and Review.objects.filter(
                    author=author, title=title_id).exists()):
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализует/десериализует данные модели Comment.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
