from django.shortcuts import render
from rest_framework.views import APIView, Request, Response, status
from rest_framework import generics
from .models import History
from django.shortcuts import get_object_or_404
from .serializers import HistorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserHistoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request: Request) -> Response:
        history_id = request.user.history.id
        history = get_object_or_404(History, id=history_id)
        serializer = HistorySerializer(history)

        return Response(serializer.data, status=status.HTTP_200_OK)