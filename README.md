библиотеки: aiogram3, sqlalchemy orm, asyncpg, environs, asyncio
БД: postgresql

ТЗ по проекту:
1. Админ - староста этажа может создавать и рассылать жителям этажа расписание уборки на кухне
2. Этажей и админом может быть несколько
3. Жители этажа подтверждают, что с расписанием ознакомлены
4. Сообщение с отчётом о подтверждении приходит админу
5. При входе в бота админ должен вводить номер своего этажа и добавлять номера комнат, жители которых будут учавствовать в уборке
6. Админ может при необходимости изменить добавленнные ранее номера комнат
7. При входе в бота пользователь и админ должены регистрироваться
8. Данные должны быть привязаны к БД
9. Пользовательно может просматривать свой профиль и расписание на конкрентную дату
