from django.shortcuts import render
from rest_framework import generics
from championships.models import Championship
from championships.permissions import IsChampionshipOwner, IsAteamOwnerAndHaveFivePlayers
from .serializers import (
    CreateChampionshipsSerializer,
    ListChampionshipsSerializer,
    ChampionshipDetailSerializer,
    RetrieveChampionShipWithGamesSerializer,
    RetrieveChampionAddingGamesSerializer,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permissions import IsStaff
from teams.models import Team
from rest_framework import views
import ipdb


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


class AddTeamsInChampionshipView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAteamOwnerAndHaveFivePlayers]
    queryset = Team.objects.all()
    lookup_url_kwarg = "team_id"
    serializer_class = ListChampionshipsSerializer
    
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        cs_id = kwargs['cs_id']
        champ_updated = Championship.objects.get(id=cs_id)
        cham_serializer = RetrieveChampionAddingGamesSerializer(champ_updated)
        # ipdb.set_trace()
        
        return_dict = {
            "detail": "Team has been added",
            "teams_in_championship": cham_serializer.data['teams']
        }
        return views.Response(return_dict)
    
    
