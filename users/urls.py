from django.urls import path, include
from users import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", views.ListUsersView.as_view()),
    path("users/register/", views.CreateUserView.as_view()),
    path("users/<str:user_id>/", views.RetrieveUpdateUserView.as_view()),
    path("users/<str:user_id>/activity/", views.UpdateActivityUserView.as_view()),
    path("login/", views.LoginView.as_view()),
]
