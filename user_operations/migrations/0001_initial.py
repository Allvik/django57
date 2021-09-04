# Generated by Django 3.2.7 on 2021-09-04 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game_operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.ManyToManyField(to='game_operations.game')),
            ],
        ),
        migrations.CreateModel(
            name='my_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('is_super_user', models.BooleanField()),
                ('my_games', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_operations.all_games')),
            ],
        ),
    ]
