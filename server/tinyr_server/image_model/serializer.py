from .models import ImageModel
from rest_framework import serializers

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["image", "profile"]


