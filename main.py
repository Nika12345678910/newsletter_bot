import logging, asyncio

from aiogram import Bot, Dispatcher

from config_data.config import load_config
from handlers.user import user_router
from handlers.admin import admin_router
from middleware.outer import OuterMiddlewareAdmin, OuterMiddlewareSession
from database.engine import session_maker, create_db, drop_db
from FSM.fsm import storage


logger = logging.getLogger(__name__)


async def startup(bot):
    #await drop_db()
    await create_db()


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s")

    config = load_config()

    bot = Bot(token=config.tg_bot.token)
    admin_ids = list(config.tg_bot.admin_ids)
    bot.admin_ids = admin_ids
    dp = Dispatcher(storage=storage)

    logger.info("Starting bot")

    dp.startup.register(startup)

    dp.include_router(user_router)
    dp.include_router(admin_router)

    admin_router.message.outer_middleware(OuterMiddlewareAdmin(admin_ids=admin_ids))
    dp.update.middleware(OuterMiddlewareSession(session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())