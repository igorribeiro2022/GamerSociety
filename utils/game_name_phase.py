from django.db import models


class Phase(models.TextChoices):
    QUARTERS_UPPER = "Quartas Upper"
    SEMI_UPPER = "Semi Upper"
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
