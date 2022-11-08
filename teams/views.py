from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from teams.models import Team
from teams.serializers import TeamSerializer, TeamDetailSerializer
from users.models import User
from .permissions import (
    IsStaff,
    isAuth,
    AlreadyHaveATeam,
    PlayerToBeAddedAlreadyHasATeam,
    CanReallyAddThisUsersInTeam,
)
from django.shortcuts import get_object_or_404
from championships.permissions import IsATeamOwner
from championships.models import Championship
from rest_framework import views
from transactions.serializers import TransactionSerializer


class ListTeamsView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CreateTeamsView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAuth, AlreadyHaveATeam]
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        user_unique = User.objects.get(id=self.request.user.id)
        user_unique.is_team_owner = True
        user_unique.save()
        users = User.objects.filter(id=self.request.user.id)
        serializer.save(users=users)


class RetrieveUpdateDeleteTeams(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class InsertUsersInTeams(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [
        IsStaff,
        PlayerToBeAddedAlreadyHasATeam,
        CanReallyAddThisUsersInTeam,
    ]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_update(self, serializer):
        get_object_or_404(User, username=self.request.user.username)
        users_to_insert = []
        for value in self.request.data.values():
            user = get_object_or_404(User, username=value)
            users_to_insert.append(user)
        serializer.save(users=users_to_insert)


class RemoveTeamFromChampionship(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, IsATeamOwner]

    queryset = Team.objects.all()
    serializer_class = [TeamSerializer]

    lookup_url_kwarg = ["team_id", "championship_id"]

    def patch(self, request, *args, **kwargs):
        champ_id = kwargs["championship_id"]
        team_id = kwargs["team_id"]
        # team = Championship.objects.get(id=champ_id).teams.values().get(id=team_id)
        team = Team.objects.get(id=team_id)
        champ = Championship.objects.get(id=champ_id)
        queryset_champ = team.championship.all()
        array = [champ for champ in queryset_champ]
        array.remove(champ)
        team.championship.set(array)
        team.save()

        prize = {"value": champ.entry_amount}

        trans = TransactionSerializer(data=prize)
        trans.is_valid(raise_exception=True)
        trans.save(user=request.user)

        return views.Response({"detail": "Team removed from this championship"})
