from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(min_length=6, write_only=True)

    def create(self, validated_data):
        email = self.validated_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already registered!")
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"]
        )    
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "date_joined")