from django.contrib.gis.db import models
from django.db.models import indexes
from users.models import User
from dateutil.relativedelta import relativedelta
import uuid
from datetime import date
# Create your models here.

# All the available GENDER_CHOICES
# Expand for further options
GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("TF", "Transfemale"),
    ("TM", "Transmale"),
    ("TG", "Transgender"),
    ("NB", "Nonbinary"),
    ("GF", "Genderfluid"),
    ("GQ", "Gender Queer"),
    ("GNC", "Gender Nonconforming"),
    ("DG", "Demigender"),
    ("DF", "Demigender-Female"),
    ("DM", "Demigender-Male"),
    ("O", "Other"),
    ("P", "Prefer not to say"),
]



# All the available body BODY_TYPES
# Expand for further options
BODY_TYPES = [
    ("T", "Thin"),
    ("A", "Athletic"),
    ("O", "Affected by Obesity"),
    ("F", "Fit"),
    ("DB", "Has a Dad Bod"),
    ("HW", "Higher Weight"),
    ("M", "Muscular"),
    ("C", "Curvy"),
    ("Av", "Average"),
    ("P", "Prefer not to say"),
]



class UserProfile(models.Model):
    """
    UserProfile model for storing user profile information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=256, choices = GENDER_CHOICES)
    verbosity = models.BooleanField()
    height = models.CharField(max_length=16)
    body_type = models.CharField(max_length=64, choices = BODY_TYPES)
    sexual_orientation = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(geography=True)
    bio = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        """
        Meta class for UserProfile model 
        """
        indexes = [
            models.Index(fields=['location'])
        ]




