from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=127, unique=True)
    birthday = models.DateField()
    is_player = models.BooleanField(blank=True, default=False, null=True)
    is_staff = models.BooleanField(blank=True, default=False, null=True)
    is_team_owner = models.BooleanField(blank=True, default=False, null=True)

    team = models.ForeignKey(
        "teams.Team",
        related_name="users",
        on_delete=models.SET_NULL,
        null=True,
    )

    REQUIRED_FIELDS = ["nickname", "birthday", "email"]
