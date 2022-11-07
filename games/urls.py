from django.urls import path
from . import views

urlpatterns = [
    path("games/", views.ListBettableGamesView.as_view()),
    path("games/<str:game_id>/", views.UpdateTeamsGameView.as_view()),
    path("games/<str:game_id>/winner/", views.UpdateGameWinnerView.as_view())
]