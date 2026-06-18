# handlers/start.py

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from database import (
    add_user,
    get_channels
)

from keyboards.user import (
    main_menu,
    subscribe_keyboard
)

from config import START_TEXT

router = Router()


async def check_subscriptions(bot, user_id):
    channels = await get_channels()

    try:
        for channel in channels:
            member = await bot.get_chat_member(
                channel[0],
                user_id
            )

            if member.status not in (
                "member",
                "administrator",
                "creator"
            ):
                return False

        return True

    except:
        return False


@router.message(CommandStart())
async def start(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    channels = await get_channels()

    if channels:

        is_subscribed = await check_subscriptions(
            message.bot,
            message.from_user.id
        )

        if not is_subscribed:

            photo = FSInputFile(
                "photos/start.jpg"
            )

            await message.answer_photo(
                photo=photo,
                caption=START_TEXT,
                reply_markup=subscribe_keyboard(
                    channels
                )
            )

            return

    await message.answer(
        "🎉 Добро пожаловать!",
        reply_markup=main_menu
    )


@router.callback_query(
    F.data == "check_sub"
)
async def check_sub(
    callback: CallbackQuery
):

    is_subscribed = await check_subscriptions(
        callback.bot,
        callback.from_user.id
    )

    if not is_subscribed:

        await callback.answer(
            "❌ Вы подписались не на все каналы",
            show_alert=True
        )

        return

    await callback.message.delete()

    await callback.message.answer(
        "✅ Подписка подтверждена!",
        reply_markup=main_menu
    )

    await callback.answer()
