


def check_c_room(param):
    if param in ('1', '2', '3', '1-2', '1-3', '2-3'):
        return True
    return False

def check_city(param):
    if param in ('Киев','Одесса','Львов','Днепр','Харьков','Запорожье','Чернигов','Черкасы','Ужгород'):
        return True
    return False

def check_sort(param):
    if param in ('Новинки', 'Дешёвые', 'Дорогие'):
        return True
    return False


# isnumeric не подходит, нужны латинский цифры
def check_num(param):
    try:
        int(param)
        return True
    except:
        return False