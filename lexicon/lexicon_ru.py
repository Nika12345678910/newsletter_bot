LEXICON = {
    "admin": "Ваши права админа подтверждены✅",
    "start": "Добро пожаловать в бота👋",
    "registration_admin": "Для использование бота необходимо зарегестрироваться😞\nПосле регистрации ещё раз введите команду /admin для подтверждения ваших прав администратора",
    "registration": 'Для использование бота необходимо зарегестрироваться😉',
    "possibilities_user": "Выберите действие",
    "first_name": "✏️Введите имя",
    "last_name": "✏️Введите фамилию",
    "room": "🔑Введите номер комнаты",
    "error_first_name": "❌Введите имя\n(имя не может превышать 20 символов и должно содержать только кириллицу)",
    "error_last_name": "❌Введите фамилию\n(фамилия не может превышать 20 символов и должна содержать только кириллицу)",
    "error_room": "❌Выедите номер комнаты. Номер может содержать только цифры. Если вышей комнаты нет среди перечисленных выше - обратитесь к старосте этажа",
    "registration_close": "Регистрация прошла успешно✅",
    "date": "📆Введите дату дежурства в формате гггг/мм/дд \nНапример 2024/10/01",
    "time": "🕰️Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "error_date": "❌Введите дату дежурства в формате гггг/мм/дд \nНапример 2024/10/01\nДату можно устанавливать начиная с текущего числа и на месяц вперёд",
    "error_time": "❌Введите время начала дежурства в формате чч:мм\nНапример 22:00",
    "add_schedule": "Расписание успешно добавлено✅",
    "check_schedule": "Проверьте составленное расписание:",
    "public_schedule": "Расписание опубликовано✅",
    "add_floor": "Введите номер этажа, старостой которого вы являетесь",
    "add_numbers_rooms": "Введите номера комнат на этаже через запятную\nПример: 100, 101, 102...",
    "add_data_headmen": "Данные успешно добавлены✅",
    "error_numbers_rooms": "❌Введите с клавиатуры номера комнат. Номера комнат не могут повторяться",
    "error_floor": "❌Этаж обозначается только цифрами",
    "change_schedule": "Начинается процесс изменения расписания",
    "start_create_schedule": "Начинается процесс создания расписания",
    "view_schedule": "Укажите дату, на которую вы ходите посмотреть расписание"
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
    "possibilities_admin": ["Просмотр расписания", "Создание расписания", "Обновление расписания", "Добавление/изменение комнат этажа"],
    "placeholder_admin_kb": "Выберите действие",
    "check_schedule": {"Подтвердить✅": "confirm",
                       "Изменить❌": "change"},
    "cancel": {"Отмена": "cancel"}
}

def check_schedule_kb(data: dict):
    return {"Подтвердить": f"confirm_{data['date']}_{data['time']}_{data['room']}",
            "Изменить": f"change_{data['date']}_{data['time']}_{data['room']}"}