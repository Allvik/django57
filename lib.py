from user_operations.models import my_user
from game_operations.models import game


def check_method_post(request):
    return request.method == "POST"


def check_method_get(request):
    return request.method == "GET"


def check_user_cookie(request):
    return "user" in request.COOKIES


def get_user(**kwargs):
    cur_users = my_user.objects.all()
    if "id" in kwargs:
        cur_users = cur_users.filter(id=kwargs['id'])
    if "nick" in kwargs:
        cur_users = cur_users.filter(nick=kwargs['nick'])
    if "password" in kwargs:
        cur_users = cur_users.filter(password=kwargs['password'])
    if len(cur_users) == 0:
        return None
    return cur_users[0]


def get_game(**kwargs):
    cur_games = game.objects.all()
    if "id" in kwargs:
        cur_games = cur_games.filter(id=kwargs['id'])
    if "name" in kwargs:
        cur_games = cur_games.filter(name=kwargs['name'])
    if "password" in kwargs:
        cur_games = cur_games.filter(password=kwargs['password'])
    if "short_name" in kwargs:
        cur_games = cur_games.filter(short_name=kwargs['short_name'])
    if len(cur_games) == 0:
        return None
    return cur_games[0]