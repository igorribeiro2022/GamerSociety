from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from teams.models import Team
from teams.serializers import TeamSerializer
from users.models import User
from .permissions import IsStaff, isAuth
from django.shortcuts import get_object_or_404

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
        
