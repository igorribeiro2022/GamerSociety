from rest_framework.serializers import ModelSerializer
from historys.models import History


class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"

    # championship = ListChampionshipsSerializer(read_only=True, allow_null=True)
    # users = UserForTeamSerializer(many=True, allow_null=True, read_only=True)
