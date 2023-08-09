from datetime import datetime

def check_c_room(param):
    if param in ('1', '2', '3', '1-2', '1-3', '2-3'):
        return True
    return False


def check_city(param):
    if param in ('Киев', 'Одесса', 'Львов', 'Днепр', 'Харьков', 'Запорожье', 'Чернигов', 'Черкасы', 'Ужгород'):
        return True
    return False


def check_sort(param):
    if param in ('Новинки', 'Дешёвые', 'Дорогие', 'Пропуск'):
        return True
    return False


def check_num(param):
    try:
        int("".join(param.replace('.', '')))  # "10.000" -> 10000
        return True
    except:
        return False


def check_time(param):
    if param is not None:
        if datetime.now() > param:
            return True
        return False
    return True


def check_max_min(max_c, min_c):
    if max_c is not None and min_c is not None:
        if max_c >= min_c:
            return True
        return False
    return True