import uuid
from django.db import models


class Bet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    initial_date = models.DateField(null=False)
    is_active = models.BooleanField(default=True, null=False)
    game = models.CharField(max_length=120, null=False)
    team_1 = models.CharField(max_length=120, null=False)
    team_2 = models.CharField(max_length=120, null=False)
    winner = models.CharField(max_length=120)
    total_value = models.FloatField()
