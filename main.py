import datetime as dt  # Импорт модуля датавремя.
from decimal import Decimal as ds

FORMAT = '%H:%M:%S'    # Формат полученного времени.
WEIGHT = 75            # Вес.
HEIGHT = 175           # Рост.
K_1 = 0.035            # Коэффициент для подсчета калорий.
K_2 = 0.029            # Коэффициент для подсчета калорий.
STEP_M = 0.65          # Длина шага в метрах.
 
storage_data = {}      # Словарь для хранения полученных данных.

def check_correct_data(data):
    # Проверка корректности полученного пакета.
    return len(data) == 2 and all(data)
    
def check_correct_time(time):
    return not(len(storage_data) != 0 and time <= max(storage_data)) 
    
def get_step_day(storage_data, steps):
    # Количество пройденных шагов за этот день.
    return sum(storage_data.values()) + steps

def get_distance(steps):
    # Дистанция пройденного пути в км.
    return (steps + sum(storage_data.values())) * STEP_M / 1000

def get_spent_calories(dist, current_time):
    # Количество потраченных калорий.
    hours = round(current_time.hour + current_time.minute / 60 + current_time.second / 3600, 2)
    mean_speed = dist / hours
    minutes = hours * 60
    spent_calories = (K_1*WEIGHT + (mean_speed**2 / HEIGHT) * K_2*WEIGHT) * minutes
    return spent_calories # Калории в минуту * 60 * кол-во часов.


def get_achievement(dist):
    # Поздравления за пройденную дистанцию.
    if dist >= 6.5:
        achievement = 'Отличный результат! Цель достигнута.'
    elif dist >= 3.9:
        achievement = 'Неплохо! День был продуктивным.'
    elif dist >= 2:
        achievement = 'Маловато, но завтра наверстаем!'
    else:
        achievement = 'Лежать тоже полезно. Главное — участие, а не победа!'
    
    return achievement

def show_message(current_time, day_steps, dist, spent_calories, achievement):
    print(f'''
Время: {current_time}.
Количество шагов за сегодня: {day_steps}.
Дистанция составила {dist:.2f} км.
Вы сожгли {spent_calories:.2f} ккал.
{achievement}
''')


def accept_package(data):
    # Обработатка входящих данных.
    if not check_correct_data(data):
        return 'Некорректный пакет'

    # Распаковка полученных данных.
    pack_time = dt.datetime.strptime(data[0], FORMAT).time()  # Время обращения
    pack_steps = data[1]                                      # Количество шагов


    if not check_correct_time(pack_time):
        return 'Некорректное значение времени'
    
    
    

    day_steps =  get_step_day(storage_data, pack_steps)   # Кол-во пройденных шагов.
    dist =  get_distance(pack_steps)                      # Пройдено, км.
    spent_calories = get_spent_calories(dist, pack_time)  # Сожжённо калорий.
    achievement =  get_achievement(dist)                  # Мотивирующее сообщение.      
    
    show_message(pack_time, day_steps, dist, spent_calories, achievement)
    storage_data[pack_time] = pack_steps
    return storage_data