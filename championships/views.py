from django.shortcuts import render
from rest_framework import generics
from championships.models import Championship
from championships.permissions import IsChampionshipOwner
from .serializers import (
    CreateChampionshipsSerializer,
    ListChampionshipsSerializer,
    ChampionshipDetailSerializer,
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
    serializer_class = ListChampionshipsSerializer
    queryset = Championship.objects.all()
    lookup_url_kwarg = "cs_id"


class CreateChampionshipsView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, IsAuthenticatedOrReadOnly]

    serializer_class = CreateChampionshipsSerializer
    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(staff_owner_id=self.request.user)


class ChampionshipDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsChampionshipOwner]
    serializer_class = ChampionshipDetailSerializer

    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(staff_owner_id=self.request.user)


class AddTeamsInChampionshipView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsChampionshipOwner]

    serializer_class = ListChampionshipsSerializer
