from django.contrib.auth.models import User
from rest_framework import serializers

from blog_auth.models import Profile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.
    """

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']


class TokenSerializer(serializers.Serializer):
    """
    Serializer for authentication tokens. Used to aid documentation generation.
    """
    refresh = serializers.CharField()
    access = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login request. Used to aid documentation generation.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
