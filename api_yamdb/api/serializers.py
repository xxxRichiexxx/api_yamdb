import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        extra_kwargs = {'name': {'required': False}}


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        extra_kwargs = {'name': {'required': False}}


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # genre = serializers.MultipleChoiceField(choices=Genre.objects.all().values_list('id', 'slug'))
    # category = serializers.ChoiceField(
    #     choices=Category.objects.all().values_list('id', 'slug'))

    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {'description': {'required': False}}

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска превышает текущий!')
        return value
