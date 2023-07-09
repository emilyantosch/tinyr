from django.db import models
from users.models import User
import uuid
# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=256)
    height = models.CharField(max_length=16)
    body_type = models.CharField(max_length=64)
    sexual_orientation = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    bio = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
