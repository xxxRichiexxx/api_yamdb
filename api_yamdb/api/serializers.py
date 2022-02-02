import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    # rating = serializers.SerializerMethodField(default=0)
    genre = serializers.ChoiceField(choices=Genre.objects.values_list('slug'))
    category = serializers.ChoiceField(
        choices=Category.objects.values_list('slug'))

    class Meta:
        model = Title
        fields = '__all__'
        extra_kwargs = {'description': {'required': False}}

    # def get_rating(self, obj):
    #     return obj.reviews__score.all()

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска превышает текущий!')
        return value
