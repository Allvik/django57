from django.contrib import admin
from user_operations.models import my_user, user_in_game

admin.site.register(my_user)
admin.site.register(user_in_game)
