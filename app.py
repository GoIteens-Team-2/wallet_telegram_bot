import os
import asyncio

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from src.handlers.history import history_router
from src.handlers.info import info_router
from src.handlers.transactions import transaction_router
from src.handlers.currency_chart import currency_chart_router 
from src.handlers.currency_exchange import currency_exchange_router

load_dotenv()

async def main():
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()

    routers = [history_router, info_router, transaction_router, currency_chart_router, currency_exchange_router]
    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())