from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Item
import logging

logger = logging.getLogger('api')

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        logger.info(f"Creating user with username {validated_data['username']}.")
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        logger.info("User created successfully.")
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        logger.info(f"Validating login for user {data['username']}.")
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            logger.warning("Invalid login credentials.")
            raise serializers.ValidationError("Invalid Credentials")
        logger.info(f"User {data['username']} validated successfully.")
        return user
