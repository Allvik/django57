from django.contrib import admin
from django.urls import path
from game_operations import views

urlpatterns = [
    path('create', views.create),
    path('enter', views.enter),
    path('<short_name>/', views.game_menu),
    path('<short_name>/standings', views.get_standings),
    path('<short_name>/answers', views.get_answers),
    path('<short_name>/start_round', views.start_round),
    path('<short_name>/send_answer', views.add_answer),
    path('<short_name>/ok', views.answer_ok),
    path('<short_name>/no', views.answer_no),
    path('<short_name>/add_admin', views.add_admin),
]
