import json
import asyncio
from config import token
from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart

dp = Dispatcher()
bot = Bot(token="TOKEN")





user_data = {}

@dp.message(CommandStart())
async def commandstart(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {"transactions": []}

    user_data[user_id]["transactions"].append(
        {
            "name": f"Transaction for user {user_id}"
        }
    )

    file_name = f"user_{user_id}_data.json"
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(user_data[user_id], file, indent=4)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())