from django.shortcuts import render
from user_operations.forms import AccountForm
from game_operations.forms import create_game_form, enter_game_form
from django.http import HttpResponseRedirect, HttpResponse
from user_operations.models import MyUser
import lib


def index(request):
    return render(request, "index.html", {'form': AccountForm})


def create_account(request):
    if not lib.check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = AccountForm(request.POST)
    if not form.is_valid() or lib.get_user(nick=form.cleaned_data['nick']) is not None:
        return HttpResponse("Некорректные данные")
    new_user = MyUser(nick=form.cleaned_data['nick'], password=form.cleaned_data['password'],
                      is_super_user=(form.cleaned_data['nick'] == 'allvik'))
    new_user.save()
    response = HttpResponseRedirect('/menu')
    response.set_cookie('user', new_user.id)
    return response


def enter_account(request):
    if not lib.check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = AccountForm(request.POST)
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
    return render(request, "menu.html", {'user': cur_user, 'games': cur_user.my_games.all(),
                                         'create_form': create_game_form, 'enter_form': enter_game_form})


def add_super_user(request):
    if not lib.check_user_cookie(request) or not lib.check_method_post(request) or not lib.check_post_args(request,
                                                                                                           'nick'):
        return HttpResponse("Вы не вошли в аккаунт, не тот метод или нет параметров")
    cur_user = lib.get_user(id=int(request.COOKIES['user']))
    if cur_user is None or not cur_user.is_super_user:
        return HttpResponse("У вас не достаточно прав")
    new_super_user = lib.get_user(nick=request.POST['nick'])
    if new_super_user is not None:
        new_super_user.become_super()
    return HttpResponseRedirect("/menu")
