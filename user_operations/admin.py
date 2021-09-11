from django.contrib import admin

from user_operations.models import MyUser, UserInGame

admin.site.register(MyUser)
admin.site.register(UserInGame)
