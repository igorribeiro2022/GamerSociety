import uuid
from django.db import models


class Bet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    initial_date = models.DateField(auto_now_add=True, blank=True)
    is_active = models.BooleanField(default=True)
    team_1 = models.CharField(max_length=120)
    team_2 = models.CharField(max_length=120)
    winner = models.CharField(max_length=120, null=True)
    total_value = models.FloatField(blank=True, default=0.0)

    game = models.OneToOneField(
        "games.Game",
        on_delete=models.CASCADE,
        related_name="bet",
    )
