from django.shortcuts import render
from rest_framework import generics
from championships.models import Championship
from .serializers import (
    CreateChampionshipsSerializer,
    ListChampionshipsSerializer,
    ChampionshipDetailSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from users.permissions import IsStaff


class ListChampionshipsView(generics.ListCreateAPIView):
    serializer_class = ListChampionshipsSerializer
    queryset = Championship.objects.all()


class CreateChampionshipsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, IsAuthenticatedOrReadOnly]

    serializer_class = CreateChampionshipsSerializer
    queryset = Championship.objects.all()


class ChampionshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_map = {
        "GET": ChampionshipDetailSerializer,
        "PATCH": ChampionshipDetailSerializer,
        "DELETE": ChampionshipDetailSerializer,
    }

    queryset = Championship.objects.all()

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)
