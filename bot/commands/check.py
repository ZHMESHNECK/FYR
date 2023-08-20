from datetime import datetime


def check_c_room(param):
    """
    проверяет валидность данных для количества комнат

    Args:
        param (_type_): сообщение пользователя

    Returns:
        _type_: True \ False
    """
    if param in ('1', '2', '3', '1-2', '1-3', '2-3'):
        return True
    return False


def check_city(param):
    """
    проверяет валидность данных для города

    Args:
        param (_type_): сообщение пользователя

    Returns:
        _type_: True \ False
    """
    if param in ('Киев', 'Одесса', 'Львов', 'Днепр', 'Харьков', 'Запорожье', 'Чернигов', 'Черкасы', 'Ужгород'):
        return True
    return False


def check_sort(param):
    """
    проверяет валидность данных для количества сортировки

    Args:
        param (_type_): сообщение пользователя

    Returns:
        _type_: True \ False
    """
    if param in ('Новинки', 'Дешёвые', 'Дорогие', 'Пропуск'):
        return True
    return False


def check_num(param):
    """
    проверяет валидность данных для числа

    Args:
        param (_type_): сообщение пользователя

    Returns:
        _type_: True \ False
    """
    try:
        int("".join(param.replace('.', '')))  # "10.000" -> 10000
        return True
    except:
        return False


def check_time(param):
    """
    проверяет валидность данных для временни

    Args:
        param (_type_): время прошлой блокировки

    Returns:
        _type_: True \ False
    """
    if param is not None:
        if datetime.now() > param:
            return True
        return False
    return True


def check_max_min(max_c, min_c):
    """
    если оба параметра int делает проверку max_c >= min_c, 

    Args:
        max_c (_type_): int
        min_c (_type_): int

    Returns:
        _type_: True \ False
    """
    if max_c is not None and min_c is not None:
        if max_c >= min_c:
            return True
        return False
    return True
