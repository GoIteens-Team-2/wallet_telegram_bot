import json
import asyncio
from config import token
from aiogram import Dispatcher, Bot, types
from aiogram.filters import CommandStart

dp = Dispatcher()
bot = Bot(token="TOKEN")

@dp.message(CommandStart())
async def commandstart(message: types.Message):
    def write_inf(data, file_name):
        data = json.dumps(data)
        data = json.loads(str(data))

        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    trunsuction = "path_to_file.json"

    data = {
        "trunsuction": []
    }

    data["trunsuction"].append(
        {
            "name": f"{trunsuction}"
        }
    )

    write_inf(data, trunsuction)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
