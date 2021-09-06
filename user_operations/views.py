from django.shortcuts import render
from user_operations.forms import account_form
from game_operations.forms import create_game_form, enter_game_form
from django.http import HttpResponseRedirect, HttpResponse
from user_operations.models import my_user, all_games
import lib


def index(request):
    return render(request, "index.html", {'form': account_form})


def create_account(request):
    if not lib.check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = account_form(request.POST)
    if not form.is_valid() or lib.get_user(nick=form.cleaned_data['nick']) is not None:
        return HttpResponse("Некорректные данные")
    new_user = my_user(nick=form.cleaned_data['nick'], password=form.cleaned_data['password'],
                                              is_super_user=form.cleaned_data['is_super_user'])
    new_user.my_games = all_games()
    new_user.my_games.save()
    new_user.save()
    response = HttpResponseRedirect('/menu')
    response.set_cookie('user', new_user.id)
    return response


def enter_account(request):
    if not lib.check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = account_form(request.POST)
    if not form.is_valid():
        return HttpResponse("Некорректные данные")
    cur_user = lib.get_user(nick=form.cleaned_data['nick'], password=form.cleaned_data['password'])
    if cur_user is None:
        return HttpResponse("Такого пользователя нет")
    response = HttpResponseRedirect('/menu')
    response.set_cookie('user', cur_user.id)
    return response


def get_menu(request):
    if not lib.check_method_get(request) or not lib.check_user_cookie(request):
        return HttpResponse("Не тот метод или нет куки")
    cur_user = lib.get_user(id=int(request.COOKIES['user']))
    if cur_user is None:
        return HttpResponse("Вас не существует")
    print(len(cur_user.my_games.games.all()))
    return render(request, "menu.html", {'nick': cur_user.nick, 'games': cur_user.my_games.games.all(),
                                         'is_super_user': cur_user.is_super_user,
                                         'create_form': create_game_form, 'enter_form': enter_game_form})
