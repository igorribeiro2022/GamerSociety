import uuid
from django.db import models
from utils.game_name_phase import Names, Phase


class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=20, choices=Names.choices, default=Names.GAME_1)
    phase = models.CharField(
        max_length=20, choices=Phase.choices, default=Phase.DEFAULT
    )
    winner = models.CharField(max_length=120, default=None, null=True)
    result_team_1 = models.IntegerField(blank=True, null=True, default=None)
    result_team_2 = models.IntegerField(blank=True, null=True, default=None)
    team_1 = models.CharField(max_length=120, blank=True, null=True, default=None)
    team_2 = models.CharField(max_length=120, blank=True, null=True, default=None)

    championship = models.ForeignKey(
        "championships.Championship",
        on_delete=models.CASCADE,
        related_name="games",
    )
