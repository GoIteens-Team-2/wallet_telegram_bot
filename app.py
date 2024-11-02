import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.deep_linking import create_start_link

from dotenv import load_dotenv

from src.handlers import (
    history_router,
    info_router,
    transaction_router,
    currency_chart_router,
    currency_exchange_router,
)

load_dotenv()


async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    link = await create_start_link(bot, "start", encode=True)
    print(link)
    routers = [
        info_router,
        history_router,
        transaction_router,
        currency_chart_router,
        currency_exchange_router,
    ]
    dp.include_routers(*routers)
    print("Test 1")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print("Test2")


if __name__ == "__main__":
    asyncio.run(main())
