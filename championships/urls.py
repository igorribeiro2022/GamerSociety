from django.urls import path
from . import views
from teams.views import RemoveTeamFromChampionship


urlpatterns = [
    path(
        "championships/list/",
        views.ListAllChampionshipsView.as_view(),
    ),  # listar todos
    path(
        "championships/register/",
        views.CreateChampionshipsView.as_view(),
    ),  # create
    path(
        "championships/<str:cs_id>/delete/",
        views.DeleteChampionshipView.as_view(),
    ),  # delete, winner patch
    path(
        "championships/<str:cs_id>/",
        views.ListOneChampionshipView.as_view(),
    ),  # list one
    path(
        "championships/<str:cs_id>/add-teams/<str:team_id>/",
        views.AddTeamsInChampionshipView.as_view(),
    ),  # nova view, serializers
    path("championships/remove/<str:team_id>/champ/<str:championship_id>/", RemoveTeamFromChampionship.as_view())
]
