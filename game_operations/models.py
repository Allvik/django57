from django.db import models


class game(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    users_information = models.ManyToManyField('user_operations.user_in_game')
    count_rounds = models.IntegerField(default=0)

    def __init(self, *args, **kwargs):
        super().__init__(args, kwargs)


