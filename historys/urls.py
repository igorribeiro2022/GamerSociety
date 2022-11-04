from django.urls import path
from historys import views


urlpatterns = [
    path(
        "balance/",
        views.UserHistoryView.as_view(),
    ),  # listar todos
]