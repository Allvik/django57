from django.shortcuts import render
from game_operations.forms import create_game_form, enter_game_form
from user_operations.models import my_user
from game_operations.models import game, users_answers
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
    answers = users_answers()
    answers.save()
    new_game = game(name=form.cleaned_data['name'], short_name=form.cleaned_data['short_name'],
                           password=form.cleaned_data['password'], count_rounds=form.cleaned_data['count_rounds'], answers=answers)

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
    if cur_game is None or cur_game in cur_user.my_games.all():
        return HttpResponse("Такой игры не существует или вы в нее уже зашли")
    cur_user.add_game(cur_game)
    return HttpResponseRedirect(f"{cur_game.short_name}")


def game_menu(request, short_name):
    if not lib.check_user_cookie(request) or not lib.check_method_get(request):
        return HttpResponse("Нет кук или не тот метод")
    cur_user = lib.get_user(id=request.COOKIES['user'])
    cur_game = cur_user.my_games.filter(short_name=short_name)
    if cur_user is None or len(cur_game) == 0:
        return HttpResponse("Такого пользователя или игры не существует")
    cur_game = cur_game[0]
    return render(request, 'game_menu.html', {'game': cur_game, 'user_in_game': cur_game.users_information.filter(user=cur_user)[0],
                            'answers': cur_game.answers.answers.all()})
