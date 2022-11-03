from django.shortcuts import render
from rest_framework import generics
from championships.models import Championship
from championships.permissions import IsChampionshipOwner, IsAteamOwnerAndHaveFivePlayers
from .serializers import (
    CreateChampionshipsSerializer,
    ListChampionshipsSerializer,
    ChampionshipDetailSerializer,
    RetrieveChampionShipWithGamesSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsStaff


class ListAllChampionshipsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, IsAuthenticatedOrReadOnly]

    serializer_class = ListChampionshipsSerializer
    queryset = Championship.objects.all()


class ListOneChampionshipView(generics.RetrieveAPIView):
    serializer_class = RetrieveChampionShipWithGamesSerializer
    queryset = Championship.objects.all()
    lookup_url_kwarg = "cs_id"


class CreateChampionshipsView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    serializer_class = CreateChampionshipsSerializer
    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(staff_owner=self.request.user)


class ChampionshipDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsChampionshipOwner]
    serializer_class = ChampionshipDetailSerializer
    lookup_url_kwarg = "cs_id"
    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(staff_owner=self.request.user)


class AddTeamsInChampionshipView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAteamOwnerAndHaveFivePlayers]
    lookup_url_kwarg = "cs_id", "team_id"
    serializer_class = ListChampionshipsSerializer
