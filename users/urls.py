from django.urls import path, include
from users import views

urlpatterns = [
    path("users/", views.ListCreateUserView.as_view()),
    path("users/<str:user_id>/", views.RetrieveUpdateUserView.as_view()),
    path("users/<str:user_id>/activity/", views.UpdateActivityUserView.as_view()),
]