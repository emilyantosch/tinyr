from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class User (AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName", "password", "email"]
    objects = BaseUserManager()

    
