from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Championship


class CreateChampionshipsSerializer(serializers.ModelSerializer):
    # games = GameSerializer(read_only=True, many=True)

    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner_id",
            "entry_amount",
            "prize",
            "teams",
            # "games",
        ]

        read_only_fields = [
            "id",
            "staff_owner_id",
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
            "staff_owner_id",
            # "teams",
            # "games",
        ]


class ChampionshipDetailSerializer(serializers.ModelSerializer):
    # games = GamesSerializers(many=True)

    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id"]
