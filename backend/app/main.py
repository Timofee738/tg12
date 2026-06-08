import asyncio
from aiogram import Bot, Dispatcher

from config import settings

from handler import get_handlers_router


async def main():
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(get_handlers_router())

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__=='__main__':
    asyncio.run(main())