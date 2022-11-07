from django.urls import path, include
from users import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("users/", views.ListUsersView.as_view()),
    path("users/register/", views.CreateUserView.as_view()),
    path("users/<str:user_id>/", views.RetrieveUpdateUserView.as_view()),
    path("users/<str:user_id>/activity/", views.UpdateActivityUserView.as_view()),
    path("login/", views.LoginView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("docs/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
