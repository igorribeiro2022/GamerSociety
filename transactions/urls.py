from django.urls import path, include
from transactions import views


urlpatterns = [
    path("transactions/", views.CreateTransaction.as_view()),

]
