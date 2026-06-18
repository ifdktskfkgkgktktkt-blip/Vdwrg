from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import (
    add_balance,
    get_user,
    set_referrer,
    get_top_referrals
)

from config import REF_REWARD

router = Router()


@router.message(F.text == "⭐ Заработать звёзды")
async def referrals_menu(message: Message):
    bot_info = await message.bot.get_me()

    ref_link = (
        f"https://t.me/"
        f"{bot_info.username}"
        f"?start={message.from_user.id}"
    )

    text = (
        "⭐ <b>Реферальная система</b>\n\n"
        "Приглашайте друзей по вашей ссылке.\n"
        "После подписки друга вы получите награду.\n\n"
        f"🎁 Награда: {REF_REWARD} ⭐\n\n"
        f"🔗 Ваша ссылка:\n{ref_link}"
    )

    await message.answer(text)


@router.message(F.text == "🏆 Топ рефералов")
async def top_referrals(message: Message):
    top = await get_top_referrals()

    if not top:
        await message.answer(
            "🏆 Пока нет участников."
        )
        return

    text = "🏆 Топ рефералов\n\n"

    for i, user in enumerate(top, start=1):

        username = (
            f"@{user[1]}"
            if user[1]
            else f"ID {user[0]}"
        )

        text += (
            f"{i}. {username} — "
            f"{user[2]} реф.\n"
        )

    await message.answer(text)


@router.message(CommandStart())
async def referral_start(message: Message):

    args = message.text.split()

    if len(args) < 2:
        return

    try:
        referrer_id = int(args[1])
    except:
        return

    if referrer_id == message.from_user.id:
        return

    user = await get_user(
        message.from_user.id
    )

    if not user:
        return

    if user[3]:
        return

    await set_referrer(
        message.from_user.id,
        referrer_id
    )

    await add_balance(
        referrer_id,
        REF_REWARD
    )
