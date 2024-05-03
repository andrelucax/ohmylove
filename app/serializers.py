from rest_framework import serializers
from .models import Cloupe, User
from django.core.exceptions import ObjectDoesNotExist

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

class CloupeCreateSerializer(serializers.Serializer):
    user1 = serializers.EmailField()
    user2 = serializers.EmailField()

    def create(self, validated_data):
        try:
            user1 = User.objects.get(email=validated_data['user1'])
            user2 = User.objects.get(email=validated_data['user2'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("One or both users does not exists")

        cloupe = Cloupe.objects.create(user1=user1, user2=user2)
        return cloupe