from django.db import models


class MyUser(models.Model):
    nick = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    is_super_user = models.BooleanField()
    my_games = models.ManyToManyField('game_operations.Game')

    def add_game(self, cur_game):
        self.my_games.add(cur_game)
        self.save()
        cur_user_in_game = UserInGame(user=self, is_user_admin=self.is_super_user, count_rounds=cur_game.count_rounds)
        cur_user_in_game.save()
        cur_game.users_information.add(cur_user_in_game)
        cur_game.save()

    def become_super(self):
        self.is_super_user = True
        for game in self.my_games.all():
            user_in_game = game.users_information.filter(user=self)[0]
            user_in_game.is_user_admin = True
            user_in_game.save()
        self.save()


class UserInGame(models.Model):
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    is_user_admin = models.BooleanField()
    user_results = models.JSONField(default=list)
    count_rounds = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.user_results) != self.count_rounds:
            for i in range(self.count_rounds):
                self.user_results.append(False)

    def answer_ok(self, num_round):
        self.user_results[num_round] = 1
        self.save()
