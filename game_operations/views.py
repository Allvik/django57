from django.shortcuts import render
from game_operations import forms
import user_operations.models
import game_operations.models
from django.http import HttpResponseRedirect, HttpResponse
import lib


def create(request):
    if 'user' not in request.COOKIES or not lib.check_method_post(request):
        return HttpResponse("Не тот метод или нет куки")
    cur_user = lib.get_user(id=int(request.COOKIES['user']))
    if cur_user is None or not cur_user.is_super_user:
        return HttpResponse("Вас не существует или у вас не достаточно прав")
    form = forms.game_form(request.POST)
    if not form.is_valid():
        return HttpResponse("Неправильная форма")
    new_game = game_operations.models.game(name=form.cleaned_data['name'], short_name=form.cleaned_data['short_name'],
                           password=form.cleaned_data['password'])
    new_game.save()
    cur_user.add_game(new_game)
    return HttpResponseRedirect(f"game/{new_game.id}")
