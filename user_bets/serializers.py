from rest_framework import serializers
from .models import UserBet
from bet_types.models import BetType
from transactions.serializers import TransactionSerializer

class UserBetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBet
        fields = [
            "value",
        ]
        
    def create(self, validated_data):
        game_obj = validated_data.pop('game')
        team_obj = validated_data.pop('team')
        user_obj = validated_data.pop('user')
        game_bet = game_obj.bet
        
        bet_type = BetType.objects.get(bet=game_bet, team=team_obj.id)
        bet_type.total_value += validated_data['value']
        bet_type.save() 
        
        prize = {"value": -validated_data['value']}

        trans = TransactionSerializer(data=prize)
        trans.is_valid(raise_exception=True)
        trans.save(user=user_obj)

        bet = UserBet.objects.create(**validated_data, user=user_obj, bet_type=bet_type)
        return bet