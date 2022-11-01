from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from teams.models import Team
from teams.serializers import TeamSerializer
from .permissions import IsStaff, isAuth

class ListTeamsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAuth]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RetrieveUpdateDeleteTeams(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
