from django.db import models
import game_operations.models


class all_games(models.Model):
    games = models.ManyToManyField(game_operations.models.game)

    def add_game(self, cur_game):
        self.games.add(cur_game)
        self.save()

    def find_game(self, short_name):
        if len(self.games.filter(short_name=short_name)) == 0:
            return None
        return self.games.filter(short_name=short_name)[0]


class my_user(models.Model):
    nick = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    is_super_user = models.BooleanField()
    my_games = models.ForeignKey(all_games, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_games = all_games()
        self.my_games.save()

    def add_game(self, cur_game):
        self.my_games.add_game(cur_game)
        self.save()

    def find_game(self, short_name):
        return self.my_games.find_game(short_name)
