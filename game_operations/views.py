from django.shortcuts import render
from game_operations.forms import create_game_form, enter_game_form
from user_operations.models import my_user, all_games
from game_operations.models import game
from django.http import HttpResponseRedirect, HttpResponse
import lib


def create(request):
    if not lib.check_user_cookie(request) or not lib.check_method_post(request):
        return HttpResponse("Не тот метод или нет куки")
    cur_user = lib.get_user(id=int(request.COOKIES['user']))
    if cur_user is None or not cur_user.is_super_user:
        return HttpResponse("Вас не существует или у вас не достаточно прав")
    form = create_game_form(request.POST)
    if not form.is_valid():
        return HttpResponse("Неправильная форма")
    if lib.get_game(short_name=form.cleaned_data['short_name']) is not None:
        return HttpResponse("Придумайте другое короткое название")
    new_game = game(name=form.cleaned_data['name'], short_name=form.cleaned_data['short_name'],
                           password=form.cleaned_data['password'])
    new_game.save()
    cur_user.add_game(new_game)
    return HttpResponseRedirect(f"{new_game.short_name}")


def enter(request):
    if not lib.check_user_cookie(request) or not lib.check_method_post(request):
        return HttpResponse("Не тот метод или нет куки")
    cur_user = lib.get_user(id=int(request.COOKIES['user']))
    if cur_user is None:
        return HttpResponse("Вас не существует")
    form = enter_game_form(request.POST)
    if not form.is_valid():
        return HttpResponse("Неправильная форма")
    cur_game = lib.get_game(short_name=form.cleaned_data['short_name'], password=form.cleaned_data['password'])
    if cur_game is None or cur_game in cur_user.my_games.games.all():
        return HttpResponse("Такой игры не существует или вы в нее уже зашли")
    cur_user.add_game(cur_game)
    return HttpResponseRedirect(f"{cur_game.short_name}")


def game_menu(request, short_name):
    return HttpResponse(f"Игра - {short_name}")
