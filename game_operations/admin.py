from django.contrib import admin
from user_operations.models import my_user, all_games

# Register your models here.
admin.site.register(my_user)
admin.site.register(all_games)
