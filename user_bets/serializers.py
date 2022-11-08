from rest_framework import serializers
from .models import UserBet
from bet_types.models import BetType
from transactions.serializers import TransactionSerializer
from bets.models import Bet


class UserBetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBet
        fields = [
            "value",
        ]

    def create(self, validated_data):

        game_obj = validated_data.pop("game")
        team_obj = validated_data.pop("team")
        user_obj = validated_data.pop("user")
        game_bet = game_obj.bet

        bet = Bet.objects.get(id=game_bet.id)
        bet.total_value += validated_data["value"]
        bet.save()

        bets_types = BetType.objects.filter(bet=game_bet)

        user_bet = None
        
        for bet_type in bets_types:
            if bet_type.team == str(team_obj.id):
                bet_type.total_value += validated_data["value"]
                bet_type.odd = bet.total_value / bet_type.total_value
                bet_type.save()
                user_bet = UserBet.objects.create(**validated_data, user=user_obj, bet_type=bet_type)

            if bet_type.total_value > 0:
                bet_type.odd = bet.total_value / bet_type.total_value
                bet_type.save()

        bet_cost = {"value": -validated_data["value"]}

        trans = TransactionSerializer(data=bet_cost)
        trans.is_valid(raise_exception=True)
        trans.save(user=user_obj)

        # bet = UserBet.objects.create(**validated_data, user=user_obj, bet_type=bet_type)
        return user_bet
