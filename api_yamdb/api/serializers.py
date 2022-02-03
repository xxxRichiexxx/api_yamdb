import datetime as dt

from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404

from reviews.validators import validate_user
from reviews.models import (Category,
                            Genre,
                            Title)

User = get_user_model()


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
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
        if User.objects.filter(~Q(email=data['email']), username=data['username']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует!')
        elif User.objects.filter(~Q(username=data['username']), email=data['email']).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!')
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user, created = User.objects.get_or_create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(source='password')

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    genre = serializers.MultipleChoiceField(choices=Genre.objects.all().values_list('id', 'slug'))
    category = serializers.ChoiceField(
        choices=Category.objects.all().values_list('id', 'slug'))

    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {'description': {'required': False}}

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска превышает текущий!')
        return value
