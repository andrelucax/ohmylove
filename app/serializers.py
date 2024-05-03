from rest_framework import serializers
from .models import Cloupe, User, CoupleMessage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

class CloupeCreateSerializer(serializers.Serializer):
    user1 = serializers.EmailField()
    user2 = serializers.EmailField()

    def create(self, validated_data):
        email1 = validated_data['user1']
        email2 = validated_data['user2']

        try:
            user1 = User.objects.get(email=email1)
            user2 = User.objects.get(email=email2)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'error': 'Invalid couple'})

        if Cloupe.objects.filter(
            Q(user1=user1) | Q(user2=user1) |
            Q(user1=user2) | Q(user2=user2)
        ).exists():
            raise serializers.ValidationError({'error': 'Invalid couple'})

        cloupe = Cloupe.objects.create(user1=user1, user2=user2)
        return cloupe
    
class CoupleMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupleMessage
        fields = ['id', 'message', 'created']