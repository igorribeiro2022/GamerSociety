from rest_framework import serializers
from .models import Bet
from games.models import Game


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = [
            "initial_date",
            "is_active",
            "team_1",
            "team_2",
            "total_value",
            "bet",
        ]
        depth = 1
