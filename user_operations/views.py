from django.shortcuts import render
from user_operations import forms
from django.http import HttpResponseRedirect, HttpResponse
import user_operations.models


def check_method_post(request):
    return request.method == "POST"


def check_method_get(request):
    return request.method == "GET"


def check_user_cookie(request):
    return "user" in request.COOKIES


def index(request):
    return render(request, "index.html", {'form': forms.account_form})


def get_user(**kwargs):
    cur_users = user_operations.models.my_user.objects.all()
    if "id" in kwargs:
        cur_users = cur_users.filter(id=kwargs['id'])
    if "nick" in kwargs:
        cur_users = cur_users.filter(nick=kwargs['nick'])
    if "password" in kwargs:
        cur_users = cur_users.filter(password=kwargs['password'])
    if len(cur_users) == 0:
        return None
    return cur_users[0]


def create_account(request):
    if not check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = forms.account_form(request.POST)
    if not form.is_valid() or get_user(nick=form.cleaned_data['nick']) is not None:
        return HttpResponse("Некорректные данные")
    new_user = user_operations.models.my_user(nick=form.cleaned_data['nick'], password=form.cleaned_data['password'],
                                              is_super_user=form.cleaned_data['is_super_user'])
    new_user.my_games = user_operations.models.all_games()
    new_user.my_games.save()
    new_user.save()
    response = HttpResponseRedirect('/menu')
    response.set_cookie('user', new_user.id)
    return response


def enter_account(request):
    if not check_method_post(request):
        return HttpResponse("Не тот тип запроса")
    form = forms.account_form(request.POST)
    if not form.is_valid():
        return HttpResponse("Некорректные данные")
    cur_user = get_user(nick=form.cleaned_data['nick'], password=form.cleaned_data['password'])
    if cur_user is None:
        return HttpResponse("Такого пользователя нет")
    response = HttpResponseRedirect('/menu')
    response.set_cookie('user', cur_user.id)
    return response


def get_menu(request):
    if not check_method_get(request) or not check_user_cookie(request):
        return HttpResponse("Не тот метод или нет куки")
    cur_user = get_user(id=int(request.COOKIES['user']))
    return render(request, "menu.html", {'nick': cur_user.nick, 'games': cur_user.my_games.games.all(),
                                         'is_super_user': cur_user.is_super_user})
