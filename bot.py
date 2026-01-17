# bot.py
import asyncio
from aiogram import Bot, Dispatcher
import config
from handlers import post_job, admin

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# include routers
dp.include_router(post_job.router)
dp.include_router(admin.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
