from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Championship


class CreateChampionshipsSerializer(serializers.ModelSerializer):
    staff_owner_id = UserSerializer(read_only=True)
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
            # "teams",
            # "games",
            # "teams_results",
        ]

        read_only_fields = [
            "id",
            # "games",
            # "teams_results",
        ]

    def create(self, validated_data):
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
            # "teams_results",
        ]


class ChampionshipDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id", "winner", "teams_results"]
