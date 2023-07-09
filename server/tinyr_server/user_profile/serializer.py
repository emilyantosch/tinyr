from .models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "age",
            "gender",
            "body_type",
            "date_of_birth",
            "location",
            "height",
            "sexual_orientation",
            "bio", 
        ]
