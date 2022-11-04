from rest_framework import serializers

from games.models import Game


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"
 
class GamesLowKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "name",
            "phase"
        ]


class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "team_1",
            "team_2",
            # "initial_date"
        ]
        read_only_fields = ["id"]
        
class GameWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "winner_id"
            "result_team_1",
            "result_team_2"
        ]
        read_only_fields = ["id"]
        
class GamesToBetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "phase"
            "team_1",
            "team_2",
            "initial_date",

        ]
        read_only_fields = [
            "id",
            "name",
            "phase"
            "team_1",
            "team_2",
            "initial_date",
        ]