import uuid
from django.db import models


class Bet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    initial_date = models.DateField()
    is_active = models.BooleanField(default=True)
    team_1 = models.CharField(max_length=120)
    team_2 = models.CharField(max_length=120)
    winner = models.CharField(max_length=120)
    total_value = models.FloatField()

    game = models.OneToOneField(
        "games.game",
        on_delete=models.CASCADE,
        related_name="bet",
    )
