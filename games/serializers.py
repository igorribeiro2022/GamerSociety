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

    