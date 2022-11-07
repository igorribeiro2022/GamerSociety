from django.urls import path
from teams import views

urlpatterns = [
    path("teams/", views.ListTeamsView.as_view()),
    path("teams/register/", views.CreateTeamsView.as_view()),
    path("teams/<str:pk>/", views.RetrieveUpdateDeleteTeams.as_view()),
    path("teams/add/<str:pk>/", views.InsertUsersInTeams.as_view()),
    path("teams/remove/<str:team_id>/champ/<str:championship_id>/", views.RemoveTeamFromChampionship.as_view())
]