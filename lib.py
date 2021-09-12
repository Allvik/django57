from user_operations.models import MyUser
from game_operations.models import Game


def check_method_post(request):
    return request.method == "POST"


def check_method_get(request):
    return request.method == "GET"


def check_user_cookie(request):
    return "user" in request.COOKIES


def get_user(**kwargs):
    cur_users = MyUser.objects.all()
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
    cur_games = Game.objects.all()
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


def get_user_and_game(request, short_name):
    if not check_user_cookie(request):
        return None, None
    cur_user = get_user(id=int(request.COOKIES['user']))
    cur_game = cur_user.my_games.filter(short_name=short_name)
    if cur_user is None or len(cur_game) == 0:
        return None, None
    cur_game = cur_game[0]
    return cur_user, cur_game


def check_post_args(request, *args):
    for i in args:
        if i not in request.POST:
            return False
    return True
