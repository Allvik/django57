from django.db import models


class game(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)