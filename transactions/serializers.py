from rest_framework.serializers import ModelSerializer
from .models import Transaction
from historys.models import History


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["value", "date", "history"]
        read_only_fields = ["date", "history"]

    def create(self, validated_data):

        user = validated_data.pop("user")
        # user_history = self.context['request'].user.history
        user_history = user.history
        # ipdb.set_trace()

        transaction = Transaction.objects.create(**validated_data, history=user_history)

        history_id = user_history.id
        history_obj = History.objects.get(id=history_id)
        history_obj.balance += validated_data["value"]
        history_obj.save()

        return transaction
