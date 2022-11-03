from rest_framework import serializers
from games.serializers import GamesSerializer
from teams.serializers import TeamSerializer
from .models import Championship


class CreateChampionshipsSerializer(serializers.ModelSerializer):

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
            # "games",
        ]

        read_only_fields = [
            "id",
            "staff_owner",
            "teams",
            # "games",
        ]

    def create(self, validated_data):
        # criar os 11 games
        return Championship.objects.create(**validated_data)


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
