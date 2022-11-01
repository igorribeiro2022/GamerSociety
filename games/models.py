import uuid
from django.db import models

class Phase(models.TextChoices):
    QUARTERS_UPPER = "Quartas Upper"
    SEMI_UPPER =  "Semi Upper"
    SEMI_LOWER = "Semi Lower"
    FINAL_UPPER = "Final Upper"
    FINAL_LOWER = "Final Lower"
    FINAL_CHAMPIONS = "Final Champions"
    DEFAULT = "Not Subscribed"

class Names(models.TextChoices):
    GAME_1 = "Game 1"
    GAME_2 = "Game 2"
    GAME_3 = "Game 3"
    GAME_4 = "Game 4"

class Game(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=20, choices=Names.choices, default=Names.GAME_1)
    phase = models.CharField(max_length=20, choices=Phase.choices, default=Phase.DEFAULT)
    winner = models.CharField(max_length=20, default=None)
    # championship = models.ForeignKey("championships.Championship", on_delete=models.CASCADE)
    result_team_1 = models.IntegerField(null=True)
    result_team_2 = models.IntegerField(null=True)
    team_1 = models.CharField(max_length=120, null=True)
    team_2 = models.CharField(max_length=120, null=True)