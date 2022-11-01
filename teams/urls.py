from django.urls import path
from teams import views

urlpatterns = [
    path("teams/", views.ListTeamsView.as_view()),
    path("teams/<str:pk>/", views.RetrieveUpdateDeleteTeams.as_view())
]