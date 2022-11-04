from django.urls import path
from . import views

urlpatterns = [
    path("games/", views.ListGamesView.as_view())
]