from django.contrib import admin
from django.urls import path
from game_operations import views

urlpatterns = [
    path('create', views.create),
    path('<short_name>/', views.game_menu)
]