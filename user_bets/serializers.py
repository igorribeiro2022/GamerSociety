from rest_framework import serializers
from .models import UserBet
from bet_types.models import BetType
from transactions.serializers import TransactionSerializer
from bets.models import Bet
from games.models import Game
from championships.models import Championship
from teams.models import Team

from django.shortcuts import get_object_or_404


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
                user_bet = UserBet.objects.create(
                    **validated_data, user=user_obj, bet_type=bet_type
                )

            if bet_type.total_value > 0:
                bet_type.odd = bet.total_value / bet_type.total_value
                bet_type.save()

        champ = get_object_or_404(Championship, id=game_obj.championship.id)
        bet_cost = {
            "value": -validated_data["value"],
            "detail": f"Aposta feita no jogo: {champ.name} - {game_obj.phase} {game_obj.name}",
        }

        trans = TransactionSerializer(data=bet_cost)
        trans.is_valid(raise_exception=True)
        trans.save(user=user_obj)

        # bet = UserBet.objects.create(**validated_data, user=user_obj, bet_type=bet_type)
        return user_bet


class ListUserBetSerializer(serializers.ModelSerializer):

    odd = serializers.SerializerMethodField()
    game_name = serializers.SerializerMethodField()
    phase = serializers.SerializerMethodField()
    championship = serializers.SerializerMethodField()
    team_betted = serializers.SerializerMethodField()
    won = serializers.SerializerMethodField()

    class Meta:
        model = UserBet
        fields = [
            "id",
            "value",
            "odd",
            "game_name",
            "phase",
            "championship",
            "team_betted",
            "won",
        ]

    def get_odd(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        return BetType.objects.get(id=bet_type_id).odd

    def get_won(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        bet_type = BetType.objects.get(id=bet_type_id)
        if bet_type.winner == None:
            return "Not defined"
        if bet_type.winner == bet_type.team:
            return True
        return False

    def get_championship(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        bet_type = BetType.objects.get(id=bet_type_id)
        champ_id = Game.objects.get(bet=bet_type.bet.id).championship.id
        champ_name = Championship.objects.get(id=champ_id).name
        return champ_name

    def get_game_name(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        bet_type = BetType.objects.get(id=bet_type_id)
        game_name = Game.objects.get(bet=bet_type.bet.id).name
        return game_name

    def get_phase(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        bet_type = BetType.objects.get(id=bet_type_id)
        game_phase = Game.objects.get(bet=bet_type.bet.id).phase
        return game_phase

    def get_team_betted(self, user_bet: UserBet):
        bet_type_id = user_bet.bet_type.id
        bet_type_team = BetType.objects.get(id=bet_type_id).team
        team_name = Team.objects.get(id=bet_type_team).name
        return team_name
