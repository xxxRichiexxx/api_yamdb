import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {'description': {'required': False}}

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска превышает текущий!')
        return value
