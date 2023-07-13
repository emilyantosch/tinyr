from django.contrib.gis.db import models
from django.db.models import indexes
from users.models import User
from dateutil.relativedelta import relativedelta
import uuid
from datetime import date
# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=256)
    height = models.CharField(max_length=16)
    body_type = models.CharField(max_length=64)
    sexual_orientation = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(geography=True)
    bio = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def calcAge(self):
        return relativedelta(date.today(), self.date_of_birth).years

    class Meta:
        indexes = [
            models.Index(fields=['location'])
        ]


# Wenn man nach Transpersonen filtern möchte,
# muss man openly trans sein. Openly Trans ist
# ein- und ausschaltbar
