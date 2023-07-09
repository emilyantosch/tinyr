from django.db import models

from user_profile.models import UserProfile
# Create your models here.
class ImageModel(models.Model):
    image = models.ImageField()
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
