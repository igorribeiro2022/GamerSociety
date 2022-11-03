from django.urls import path
from . import views


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
        "championships/<str:pk>/management/",
        views.ChampionshipDetailView.as_view(),
    ),  # delete, winner patch
    path(
        "championships/<str:cs_id>/",
        views.ListOneChampionshipView.as_view(),
    ),  # list one
    path(
        "championships/<str:cs_id>/add-teams/",
        views.AddTeamsInChampionshipView.as_view(),
    ),  # nova view, serializers
]
