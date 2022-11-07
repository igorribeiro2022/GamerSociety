from rest_framework import serializers
from games.models import Game
from championships.models import Championship

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
    team_1 = serializers.CharField()
    team_2 = serializers.CharField()
    initial_date = serializers.DateField()
    class Meta:
        model = Game
        fields = [
            "id",
            "team_1",
            "team_2",
            "initial_date",
            "championship",
        ]
        read_only_fields = ["id", "championship"]
        
class GameWinnerSerializer(serializers.ModelSerializer):
    winner = serializers.CharField(max_length=120)
    result_team_1 = serializers.IntegerField()
    result_team_2 = serializers.IntegerField()

    class Meta:
        model = Game
        fields = [
            "id",
            "winner",
            "result_team_1",
            "result_team_2",
            "team_1",
            "team_2",
            "phase",
            "championship",
        ]
        read_only_fields = ["id", "phase", "championship"]
        
class BettableGamesChampionshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = ["id", "name"]
        read_only_fields = ["id"]
        
        
class GamesToBetSerializer(serializers.ModelSerializer):
    
    championship = BettableGamesChampionshipSerializer()
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "phase",
            "team_1",
            "team_2",
            "initial_date",
            "championship",

        ]
        read_only_fields = [
            "id",
            "name",
            "phase",
            "team_1",
            "team_2",
            "initial_date",
            "championship",
        ]