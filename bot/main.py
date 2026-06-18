import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN

from handlers.start import router as start_router
from handlers.profile import router as profile_router
from handlers.referrals import router as referrals_router
from handlers.bonus import router as bonus_router
from handlers.promocodes import router as promocodes_router
from handlers.withdraw import router as withdraw_router
from handlers.admin import router as admin_router

from database import init_db

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


async def startup():
    await init_db()
    print("Bot started")


def register_routers():
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(referrals_router)
    dp.include_router(bonus_router)
    dp.include_router(promocodes_router)
    dp.include_router(withdraw_router)
    dp.include_router(admin_router)


async def main():
    await startup()

    register_routers()

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
