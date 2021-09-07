from django.db import models
import django.utils.timezone


class user_answer(models.Model):
    num_round = models.IntegerField(default=0)
    answer = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class users_answers(models.Model):
    answers = models.ManyToManyField('users_answers')


class game(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    users_information = models.ManyToManyField('user_operations.user_in_game')
    count_rounds = models.IntegerField(default=0)
    cur_round = models.IntegerField(default=1)
    round_started = models.BooleanField(default=False)
    time_last_round_start = models.DateTimeField(default=django.utils.timezone.now)
    answers = models.ForeignKey('users_answers', on_delete=models.CASCADE, default=0)

    def __init(self, *args, **kwargs):
        super().__init__(args, kwargs)


