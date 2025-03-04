import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.db import init_db
from src.roles import owner, user
from src.utils import setup_logger

logger = setup_logger(__name__)


async def create_db():
    await init_db("data/val_set_clarify.json", drop=True)
    await init_db("data/train_set_clarify.json", drop=False)


async def main():
    # await create_db()
    # return
    dp = Dispatcher()
    dp.include_routers(owner, user)

    bot = Bot(
        token=os.getenv("TOKEN_BOT"),
        default=DefaultBotProperties(parse_mode="html"),
    )
    logger.info("Старт бота")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Работа приложения прервана")
    except Exception as ex:
        logger.critical(ex)
