from django.contrib import admin
from django.urls import path
from game_operations import views

urlpatterns = [
    path('create', views.create),
    path('enter', views.enter),
    path('<short_name>/', views.game_menu),
    path('<short_name>/standings', views.get_standings)
]