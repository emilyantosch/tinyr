from django.db import models
import uuid
from users.models import User


# Create your models here.
class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    p_a = models.ForeignKey(
        User, related_name="person_a_match", on_delete=models.CASCADE
    )
    p_b = models.ForeignKey(
        User, related_name="person_b_match", on_delete=models.CASCADE
    )
    p_a_fulfilled = models.BooleanField()
    p_b_fulfilled = models.BooleanField()
    match_time = models.DateTimeField()

    class Meta:
        ordering = ["match_time"]
