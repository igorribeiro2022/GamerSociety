from django.db import models
import uuid


class History(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    balance = models.FloatField(default=0.00)
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="history",
    )
