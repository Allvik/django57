from django.shortcuts import render
from game_operations.forms import create_game_form, enter_game_form
from game_operations.models import Game, UserAnswer
from django.http import HttpResponseRedirect, HttpResponse
import lib
import django.utils.timezone


def update_game_state(cur_game):
    if not cur_game.round_started:
        return
    now = django.utils.timezone.now()
    if (now - cur_game.time_last_round_start).total_seconds() >= 60:
        cur_game.round_started = False
        cur_game.cur_round += 1
        cur_game.save()


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
    new_game = Game(name=form.cleaned_data['name'], short_name=form.cleaned_data['short_name'],
                    password=form.cleaned_data['password'], count_rounds=form.cleaned_data['count_rounds'])

    new_game.save()
    cur_user.add_game(new_game)
    return HttpResponseRedirect(f"/game/{new_game.short_name}")


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
    return HttpResponseRedirect(f"/game/{cur_game.short_name}")


def game_menu(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not lib.check_method_get(request):
        return HttpResponse("Вас не существует или не тот метод")
    update_game_state(cur_game)
    return render(request, 'game_menu.html',
                  {'game': cur_game, 'user_in_game': cur_game.users_information.filter(user=cur_user)[0],
                   'answers': cur_game.answers.all()})


def get_standings(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not lib.check_method_get(request):
        return HttpResponse("Вас не существует или не тот метод")
    update_game_state(cur_game)
    results = cur_game.get_results()
    results.sort(key=lambda x: -sum(x.user_results))
    return render(request, 'standings.html', {'results': results})


def get_answers(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not cur_game.users_information.filter(user=cur_user)[0].is_user_admin \
            or not lib.check_method_get(request):
        return HttpResponse("Вы не обладаете нужными правами или не тот метод")
    update_game_state(cur_game)
    return render(request, 'answers.html', {'answers': cur_game.answers.all()})


def start_round(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not cur_game.users_information.filter(user=cur_user)[0].is_user_admin or \
            not lib.check_method_post(request):
        return HttpResponse("Вы не обладаете нужными правами или не тот метод")
    update_game_state(cur_game)
    if cur_game.round_started:
        return HttpResponse("Сейчас уже идет раунд")
    cur_game.time_last_round_start = django.utils.timezone.now()
    cur_game.round_started = True
    cur_game.save()
    return HttpResponseRedirect(f"/game/{short_name}")


def add_answer(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or cur_game.users_information.filter(user=cur_user)[0].is_user_admin \
            or not lib.check_method_post(request) or not lib.check_post_args(request, 'answer'):
        return HttpResponse("Вы не обладаете нужными правами, не тот метод или нет ответа")
    update_game_state(cur_game)
    if not cur_game.round_started:
        return HttpResponse("Вы не успели(")
    user_in_game = cur_game.users_information.filter(user=cur_user)[0]
    cur_answer = UserAnswer(num_round=cur_game.cur_round, answer=request.POST['answer'], user=user_in_game)
    cur_answer.save()
    cur_game.answers.add(cur_answer)
    cur_game.save()
    return HttpResponseRedirect(f"/game/{short_name}")


def answer_ok(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not cur_game.users_information.filter(user=cur_user)[0].is_user_admin \
            or not lib.check_method_post(request) or \
            not lib.check_post_args(request, 'answer_id') or not request.POST["answer_id"].isdigit():
        return HttpResponse("Вас не существует, не тот метод, или неправильный аргумент")
    cur_game.answer_ok(int(request.POST["answer_id"]))
    return HttpResponseRedirect(f"/game/{short_name}/answers")


def answer_no(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not cur_game.users_information.filter(user=cur_user)[0].is_user_admin \
            or not lib.check_method_post(request) or \
            not lib.check_post_args(request, 'answer_id') or not request.POST["answer_id"].isdigit():
        return HttpResponse("Вас не существует, не тот метод, или неправильный аргумент")
    cur_game.answer_no(int(request.POST["answer_id"]))
    return HttpResponseRedirect(f"/game/{short_name}/answers")


def add_admin(request, short_name):
    cur_user, cur_game = lib.get_user_and_game(request, short_name)
    if cur_user is None or not cur_game.users_information.filter(user=cur_user)[0].is_user_admin \
            or not lib.check_method_post(request) or not lib.check_post_args(request, 'nick'):
        return HttpResponse("У вас недостаточно прав для этого, не тот метод или нет аргумента")
    new_admin = lib.get_user(nick=request.POST['nick'])
    if new_admin is None or len(new_admin.my_games.filter(short_name=short_name)) == 0:
        return HttpResponse("Такого ника не существует или он не вошел в эту игру")
    new_admin_in_game = cur_game.users_information.filter(user=new_admin)[0]
    new_admin_in_game.is_user_admin = True
    new_admin_in_game.save()
    return HttpResponseRedirect(f"/game/{short_name}")
