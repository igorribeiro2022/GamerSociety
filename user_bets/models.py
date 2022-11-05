from django.db import models
import uuid

class UserBet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    value = models.FloatField()
    bet_type = models.ForeignKey(
        "bet_types.BetType",
        on_delete=models.CASCADE,
        related_name="users_bets",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bets",
    )

