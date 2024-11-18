LEXICON = {
    "admin": "Ваши права админа подтверждены",
    "start": "Добро пожаловать в бота",
    "registration": 'Для использование бота необходимо зарегестрироваться',
    "possibilities_user": "Выберите действие",
    "first_name": "Введите имя",
    "last_name": "Введите фамилию",
    "room": "Введите номер комнаты",
    "error_first_name": "Введите имя\n(имя не может превышать 20 символов и должно содержать только кириллицу)",
    "error_last_name": "Введите фамилию\n(фамилия не может превышать 20 символов и должна содержать только кириллицу)",
    "error_room": "Выберите номер комнаты из предложенных выше",
    "registration_close": "Регистрация прошла успешно",
    "date": "Введите дату дежурства в формате гггг/мм/дд \nНапример 2024/10/01",
    "time": "Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "error_date": "Введите дату дежурства в формате гггг/мм/дд \nНапример 2024/10/01",
    "error_time": "Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "add_schedule": "Расписание успешно добавлено",
    "check_schedule": "Проверьте составленное расписание:",
    "public_schedule": "Расписание опубликовано"
}


def format_profile(first_name, last_name, room):
    return f'Имя: {first_name}\nФамилия: {last_name}\nКомната: {room}'


def format_schedule(date, time, room):
    return f'Дата: {date} \nВремя: {time} \nКомната: {room}'


btns = {
    "registation": {
        "Регистрация": "registration"
        },
    "possibilities_user": {
        "Просмотр профиля": "profile",
        "Просмотр расписания": "view schedule"
        },
    "rooms": ["101", "121", "220", "332"],
    "possibilities_admin": ["Просмотр расписания", "Создание расписания", "Обновление расписания"],
    "placeholder_admin_kb": "Выберите действие",
    "check_schedule": {"Подтвердить": "confirm",
                       "Изменить": "change"}
}

def check_schedule_kb(data: dict):
    return {"Подтвердить": f"confirm_{data['date']}_{data['time']}_{data['id_room']}",
            "Изменить": f"change_{data['date']}_{data['time']}_{data['id_room']}"}