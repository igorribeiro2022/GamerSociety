import black
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20)
    balance = models.FloatField(blank=True, default=0.00)
    email = models.EmailField(max_length=127, unique=True)
    birthday = models.DateField()
    is_player = models.BooleanField(blank=True, default=False, null=True)
    team_id = models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="users", null=True)
    is_staff = models.BooleanField(blank=True, default=False)
