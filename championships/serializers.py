from rest_framework import serializers
from games.models import Game
from teams.serializers import TeamSerializer
from .models import Championship
from utils.game_name_phase import Names, Phase, games_list
from games.serializers import GamesSerializer, GamesLowKeysSerializer


class CreateChampionshipsSerializer(serializers.ModelSerializer):

    games = GamesLowKeysSerializer(read_only=True, many=True)


    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner",
            "entry_amount",
            "prize",
            "teams",
            "games",
        ]

        read_only_fields = [
            "id",
            "staff_owner",
            "teams",

        ]

    def create(self, validated_data):
        champ_created = Championship.objects.create(**validated_data)
        
        for game in games_list:
            Game.objects.create(**game, championship=champ_created)

        return champ_created
        
        


class ListChampionshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner",
            # "teams",
            # "games",
        ]


class ChampionshipDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id"]


class RetrieveChampionShipWithGamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id"]

    games = GamesSerializer(many=True)
    teams = TeamSerializer(many=True)
