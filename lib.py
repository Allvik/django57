import user_operations.models


def check_method_post(request):
    return request.method == "POST"


def check_method_get(request):
    return request.method == "GET"


def check_user_cookie(request):
    return "user" in request.COOKIES


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
