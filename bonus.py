# handlers/bonus.py

import time

from aiogram import Router, F
from aiogram.types import (
    Message,
    FSInputFile
)

from database import (
    add_balance,
    get_balance
)

from config import (
    DAILY_BONUS
)

router = Router()

bonus_users = {}


@router.message(
    F.text == "🎁 Бонус"
)
async def bonus(
    message: Message
):

    user_id = message.from_user.id

    now = int(time.time())

    if user_id in bonus_users:

        last_bonus = bonus_users[user_id]

        if now - last_bonus < 86400:

            hours = (
                86400 -
                (now - last_bonus)
            ) // 3600

            await message.answer(
                f"❌ Бонус уже получен.\n\n"
                f"⏳ Повторно через {hours} ч."
            )

            return

    bonus_users[user_id] = now

    await add_balance(
        user_id,
        DAILY_BONUS
    )

    balance = await get_balance(
        user_id
    )

    text = (
        "🎁 <b>Ежедневный бонус</b>\n\n"
        f"⭐ Начислено: {DAILY_BONUS}\n"
        f"💰 Баланс: {balance}"
    )

    try:

        photo = FSInputFile(
            "photos/bonus.jpg"
        )

        await message.answer_photo(
            photo=photo,
            caption=text
        )

    except:

        await message.answer(
            text
        )