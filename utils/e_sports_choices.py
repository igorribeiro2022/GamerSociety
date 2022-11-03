from django.db import models


class ESportChoices(models.TextChoices):
    LEAGUEOFLEGENDS = "League of Legends"
    OVERWATCH = "Overwatch"
    COUNTERSTRIKE = "Counter Strike"
    VALORANT = "Valorant"
    DEFAULT = "Is not in a championship"
