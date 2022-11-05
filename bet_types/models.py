from django.db import models
import uuid

class BetType(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    total_value = models.FloatField(blank=True, default=0.0)
    odd = models.FloatField(blank=True, default=0.0)
    team = models.CharField(max_length=120)
    winner = models.CharField(max_length=120, default=None, null=True, blank=True)

    bet = models.ForeignKey(
        "bets.Bet",
        on_delete=models.CASCADE,
        related_name="bet_types",
    )
