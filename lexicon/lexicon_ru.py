LEXICON = {
    "admin": "✅Ваши права админа подтверждены",
    "start": "Добро пожаловать в бота👋",
    "registration_admin": "Для использование бота необходимо зарегестрироваться😞\n\nПосле регистрации ещё раз введите команду /admin для подтверждения ваших прав администратора",
    "registration": 'Для использование бота необходимо зарегестрироваться',
    "possibilities_user": "Выберите действие",
    "first_name": "✏️Введите имя",
    "last_name": "✏️Введите фамилию",
    "room": "🔑Введите номер комнаты",
    "error_first_name": "❌Введите имя\n\n📌Имя не может превышать 20 символов \n📌Имя должно содержать только кириллицу",
    "error_last_name": "❌Введите фамилию\n📌Фамилия не может превышать 20 символов \n📌Фамилия должна содержать только кириллицу",
    "error_room": "❌Введите номер комнаты \n\n📌Номер может содержать только цифры \n📌Если вышей комнаты нет среди перечисленных выше - обратитесь к старосте этажа",
    "registration_close": "✅Регистрация прошла успешно",
    "date": "📆Введите дату дежурства в формате гггг-мм-дд \nНапример 2024-10-01",
    "time": "🕰️Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "error_date": "❌Введите дату дежурства в формате гггг-мм-дд \nНапример 2024-10-01 \n\n📌Дату можно устанавливать начиная с текущего числа и на месяц вперёд",
    "error_time": "❌Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "add_schedule": "✅Расписание успешно добавлено",
    "check_schedule": "Проверьте составленное расписание:",
    "public_schedule": "✅Расписание опубликовано",
    "add_floor": "Введите номер этажа, старостой которого вы являетесь",
    "add_numbers_rooms": "Введите номера комнат на этаже через запятную\nПример: 100, 101, 102...",
    "add_data_headmen": "✅Данные успешно добавлены",
    "error_numbers_rooms": "❌Введите с клавиатуры номера комнат \n\n📌Номера комнат не могут повторяться",
    "error_floor": "❌Введите номер этажа📌Этаж обозначается только цифрами \n📌Номер этажа не может повторять уже созданный",
    "change_schedule": "Начинается процесс изменения расписания...",
    "start_create_schedule": "Начинается процесс создания расписания...",
    "view_schedule": "📆Укажите дату, на которую вы ходите посмотреть расписание",
    "change_rooms": "Ранее вы добавили такие комнаты",
    "not date": "Расписание на эту дату ещё не добавили...",
    "not rooms": "Комнаты ещё не зарегестрированны админом"
}


def format_profile(first_name, last_name, room):
    return f'Профиль пользователя: \nИмя: {first_name}\nФамилия: {last_name}\nКомната: {room}'


def format_schedule(date, time, room):
    return f'Расписание на {date}: \nВремя: {time} \nКомната: {room}'


btns = {
    "registation": {
        "Регистрация": "registration"
        },
    "possibilities_user": {
        "Просмотр профиля": "profile",
        "Просмотр расписания": "view schedule"
        },
    "possibilities_admin": ["Главное меню", "Создание расписания", "Добавление/изменение комнат этажа"],
    "placeholder_admin_kb": "Выберите действие",
    "check_schedule": {"Подтвердить✅": "confirm",
                       "Изменить❌": "change"},
    "cancel": {"Отмена": "cancel"},
    "main_menu": {"К главному меню": "main_menu"}
}

def check_schedule_kb(data: dict):
    return {"Подтвердить": f"confirm_{data['date']}_{data['time']}_{data['room']}",
            "Изменить": f"change_{data['date']}_{data['time']}_{data['room']}"}


def confirm_schedule(date: str, id_chat: int, id_floor: int):
    return {"Подтвердить, что увидел": f"confirm_schedule_{date}_{str(id_chat)}_{str(id_floor)}"}


def format_user_schedule_confirmation(first_name: str,
                                      last_name: str,
                                      room: int,
                                      date: str):
    return f"{first_name} {last_name} из комнаты {room} подтвердил расписани на {date}"