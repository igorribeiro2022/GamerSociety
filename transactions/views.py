from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .serializers import TransactionSerializer
from .permissions import UserIsHistoryOwner
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from historys.models import History


class CreateTransaction(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, UserIsHistoryOwner]
    serializer_class = TransactionSerializer
    # lookup_url_kwarg = "his_id"
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

        return serializer.data
