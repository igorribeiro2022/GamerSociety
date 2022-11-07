from django.db import models
from datetime import datetime
import uuid


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    history = models.ForeignKey(
        "historys.History",
        on_delete=models.CASCADE,
        related_name="transactions",
    )
