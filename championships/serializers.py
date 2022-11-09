from rest_framework import serializers
from games.models import Game
from teams.serializers import TeamSerializer, TeamSerializerReturn, TeamsForChampSerializer
from .models import Championship
from utils.game_name_phase import Names, Phase, games_list
from utils.e_sports_choices import ESportChoices
from teams.models import Team
from games.serializers import GamesSerializer, GamesLowKeysSerializer, GamesForChampSerializer


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


class AddTeamOnChampionshipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner",
            "teams",
            "games",
            "teams",
        ]
        read_only_fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner",
            "teams",
        ]

        read_only_fields = [
            "id",
            "name",
            "initial_date",
            "e_sport",
            "winner",
            "staff_owner",
            "teams",
        ]

    def update(self, instance, validated_data):
        cs_id = self.context["view"].kwargs["cs_id"]
        championship = Championship.objects.get(id=cs_id)
        instance.championship.add(championship)
        instance.save()
        champ_updated = Championship.objects.get(id=cs_id)

        return champ_updated


class ChampionshipDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id"]
        
class ListAllChampionshipsSerializer(serializers.ModelSerializer):
    teams_in_champ = serializers.SerializerMethodField()
    class Meta:
        model = Championship
        fields = [
            "id",
            "name",
            "entry_amount",
            "prize",
            "initial_date",
            "e_sport",
            "teams_in_champ"
            ]
        read_only_fields = [
            "id",
            "name",
            "entry_amount",
            "prize",
            "initial_date",
            "e_sport",
            "teams_in_champ"
            ]
    def get_teams_in_champ(self, champ: Championship):
        return champ.teams.count()



class RetrieveChampionShipWithGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Championship
        fields = "__all__"
        read_only_fields = ["id"]

    games = GamesForChampSerializer(many=True)
    teams = TeamsForChampSerializer(many=True)


class RetrieveChampionAddingGamesSerializer(RetrieveChampionShipWithGamesSerializer):

    # games = GamesSerializer(many=True)
    teams = TeamSerializerReturn(many=True)
    
    
