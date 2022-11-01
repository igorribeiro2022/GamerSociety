from django.urls import path
from . import views


urlpatterns = [
    path("championships/list/", views.ListChampionshipsView.as_view()),
    path("championships/register/", views.CreateChampionshipsView.as_view()),
    path("championships/<int:cs_id>/", views.ChampionshipDetailView.as_view()),
]
