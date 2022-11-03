from django.db import models
from utils.e_sports_choices import ESportChoices
import uuid


class Team(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    initials = models.CharField(max_length=5)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    e_sports = models.CharField(
        max_length=50,
        choices=ESportChoices.choices,
        default=ESportChoices.DEFAULT,
    )

    championship = models.ManyToManyField(
        "championships.Championship",
        related_name="teams",
        null=True,
    )
