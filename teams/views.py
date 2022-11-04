from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from teams.models import Team
from teams.serializers import TeamSerializer
from users.models import User
from .permissions import IsStaff, isAuth, AlreadyHaveATeam, PlayerToBeAddedAlreadyHasATeam, CanReallyAddThisUsersInTeam
from django.shortcuts import get_object_or_404
import ipdb

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
    serializer_class = TeamSerializer

class InsertUsersInTeams(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff, PlayerToBeAddedAlreadyHasATeam, CanReallyAddThisUsersInTeam]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_update(self, serializer):
        get_object_or_404(User, username=self.request.user.username)
        users_to_insert = []
        for value in self.request.data.values():
            user = get_object_or_404(User, username=value)
            users_to_insert.append(user)
        serializer.save(users=users_to_insert)
        
