import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router

from keyboards.inline.start import start_router
from services.youtube_downloader import printVideo_res


bot = Bot(token="5701644076:AAEEGzP1YeveckiPH1ZYK3mDaHgHQrtT5kg", parse_mode="HTML")


async def main():
    dp = Dispatcher()
    main_router = Router()

    dp.include_router(start_router)
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
