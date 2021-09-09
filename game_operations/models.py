from django.db import models
import django.utils.timezone


class User_answer(models.Model):
    num_round = models.IntegerField(default=0)
    answer = models.CharField(max_length=100)
    user = models.ForeignKey('user_operations.User_in_game', on_delete=models.CASCADE)


class Game(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    users_information = models.ManyToManyField('user_operations.User_in_game')
    count_rounds = models.IntegerField(default=0)
    cur_round = models.IntegerField(default=1)
    round_started = models.BooleanField(default=False)
    time_last_round_start = models.DateTimeField(default=django.utils.timezone.now)
    answers = models.ManyToManyField('User_answer')

    def get_results(self):
        results = []
        for i in self.users_information.all():
            results.append(i)
        return results
