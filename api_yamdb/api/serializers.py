from rest_framework import serializers
from yamdb.validators import validate_user

from django.contrib.auth import get_user_model

User = get_user_model()


class GetConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_user]
    )
    email = serializers.EmailField(
        max_length=254,
    )
    # class Meta:
    #     model = User
    #     fields = ['email', 'username',]
    #     extra_kwargs = {'email': {'required': True}}
    #
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user


class GetTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(source='password')
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')