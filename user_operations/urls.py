from django.contrib import admin
from django.urls import path
from user_operations import views

urlpatterns = [
    path('', views.index),
    path('create_account', views.create_account),
    path('enter_account', views.enter_account),
    path('menu', views.get_menu)
]
