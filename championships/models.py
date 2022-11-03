import uuid
from django.db import models


class Championship(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=120, unique=True)
    initial_date = models.DateField()
    e_sport = models.CharField(max_length=50)
    winner = models.CharField(max_length=50, blank=True, null=True)
    entry_amount = models.FloatField()
    prize = models.FloatField()

    staff_owner_id = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="championships",
    )
