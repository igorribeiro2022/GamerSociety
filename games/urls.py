from django.urls import path
from . import views

urlpatterns = [
    path("games/", views.ListGamesView.as_view()),
    path("games/<pk>/", views.RetrieveUpdateDeleteGameView.as_view())
]