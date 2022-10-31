from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from teams.models import Team
from teams.serializers import TeamSerializer
from .permissions import IsStaff

class ListTeamsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class RetrieveUpdateDeleteTeams(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsStaff]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
