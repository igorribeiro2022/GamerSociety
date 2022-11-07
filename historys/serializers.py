from rest_framework.serializers import ModelSerializer
from historys.models import History
from transactions.serializers import TransactionForBalanceSerializer


class HistorySerializer(ModelSerializer):
    
    transactions = TransactionForBalanceSerializer(many=True)
    class Meta:
        model = History
        fields = ["balance", "transactions"]

    # championship = ListChampionshipsSerializer(read_only=True, allow_null=True)
    # users = UserForTeamSerializer(many=True, allow_null=True, read_only=True)
