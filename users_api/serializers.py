from rest_framework import serializers
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
                'read_only': True
            }
        }

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
