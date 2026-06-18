# handlers/profile.py

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from database import (
    get_balance,
    get_user
)

from keyboards.user import (
    main_menu
)

router = Router()


@router.message(
    F.text == "👤 Мой профиль"
)
async def profile(
    message: Message
):

    user = await get_user(
        message.from_user.id
    )

    balance = await get_balance(
        message.from_user.id
    )

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "Не установлен"
    )

    referrals = 0

    if user:
        referrals = user[4]

    text = (
        "👤 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"🔗 Username: {username}\n"
        f"⭐ Баланс: {balance}\n"
        f"👥 Рефералов: {referrals}"
    )

    try:
        photo = FSInputFile(
            "photos/profile.jpg"
        )

        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=main_menu
        )

    except:

        await message.answer(
            text,
            reply_markup=main_menu
        )