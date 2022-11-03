from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from teams.models import Team
from teams.serializers import TeamSerializer
from users.models import User
from users.serializers import UserSerializer
from .permissions import IsStaff, isAuth
from django.shortcuts import get_object_or_404

class ListTeamsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isAuth]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        print()
        print("="*50)
        print(self.request.user)
        print(self.request.user.is_team_owner)
        self.request.user.is_team_owner = True
        self.request.user.save()
        print(self.request.user.is_team_owner)
        print("="*50)
        print()
        serializer.save()

class RetrieveUpdateDeleteTeams(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class InsertUsersInTeams(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsStaff]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_update(self, serializer):
        request_user = get_object_or_404(User, username=self.request.user.username)
        users_to_insert = [request_user]
        for value in self.request.data.values():
            user = get_object_or_404(User, username=value)
            users_to_insert.append(user)
        serializer.save(users=users_to_insert)
        
