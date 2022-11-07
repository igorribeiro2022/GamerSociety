from django.urls import path
from . import views
from user_bets.views import CreateUserBetView

urlpatterns = [
    path("games/", views.ListBettableGamesView.as_view()),
    path("games/<str:game_id>/", views.UpdateTeamsGameView.as_view()),
    path("games/<str:game_id>/retrieve/", views.RetrieveGameView.as_view()),
    path("games/<str:game_id>/winner/", views.UpdateGameWinnerView.as_view()),
    path("games/<str:game_id>/bet/<str:team_id>/", CreateUserBetView.as_view() ),
]