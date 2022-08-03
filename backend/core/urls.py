from django.urls import path
from . import views


urlpatterns = [
    path("", views.health, name="index"),
    path("scenarios/", views.scenarios, name="scenarios"),
    path("scenarios/<int:pk>/", views.scenario, name="scenario"),
]