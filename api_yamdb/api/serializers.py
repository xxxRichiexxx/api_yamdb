from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username',]
        extra_kwargs = {'email': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
