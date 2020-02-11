from rest_framework import serializers
from django.contrib.auth import password_validation
from users_api import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ['id', 'email', 'name', 'phone', 'user_type', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
            'user_type': {
                'style': {
                    'placeholder': "Consumer / Service Provider"
                }
            }
        }

    def validate_password(self, password):
        """Validate Password"""
        password_validation.validate_password(password, self.instance)
        return password

    def validate(self, data):
        """Validate phone field"""
        if not data['phone'].isnumeric():
            raise serializers.ValidationError("Please enter a valid phone number.")
        elif len(data['phone']) != 10:
            raise serializers.ValidationError("Ensure phone length is of 10 digits.")
        elif data['user_type'] not in ('Consumer', 'Service Provider'):
            raise serializers.ValidationError("Ensure user type is only either a 'consumer' or a 'service provider'.")
        else:
            return data

    def create(self, validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            phone=validated_data['phone']
        )
        return user
