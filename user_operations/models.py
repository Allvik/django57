from django.db import models
import json


class my_user(models.Model):
    nick = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    is_super_user = models.BooleanField()
    my_games = models.ManyToManyField('game_operations.game')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_game(self, cur_game):
        self.my_games.add(cur_game)
        self.save()
        cur_user_in_game = user_in_game(user=self, is_user_admin=self.is_super_user, count_rounds=cur_game.count_rounds)
        cur_user_in_game.save()
        cur_game.users_information.add(cur_user_in_game)
        cur_game.save()

    def find_game(self, short_name):
        return self.my_games.objects.filter(short_name=short_name)


class user_in_game(models.Model):
    user = models.ForeignKey('my_user', on_delete=models.CASCADE)
    is_user_admin = models.BooleanField()
    user_results = models.JSONField(default=list)
    count_rounds = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(self.count_rounds):
            self.user_results.append(False)
