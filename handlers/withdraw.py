# handlers/withdraw.py

from aiogram import Router, F
from aiogram.types import Message

from database import (
    get_balance,
    remove_balance
)

from keyboards.user import (
    withdraw_keyboard,
    main_menu
)

router = Router()

WITHDRAW_AMOUNTS = {
    "⭐ 15": 15,
    "⭐ 25": 25,
    "⭐ 50": 50,
    "⭐ 100": 100
}


@router.message(
    F.text == "📤 Вывести звёзды"
)
async def withdraw_menu(
    message: Message
):
    await message.answer(
        "📤 Выберите количество звёзд для вывода:",
        reply_markup=withdraw_keyboard
    )


@router.message(
    F.text.in_(
        [
            "⭐ 15",
            "⭐ 25",
            "⭐ 50",
            "⭐ 100"
        ]
    )
)
async def create_withdraw(
    message: Message
):

    if not message.from_user.username:

        await message.answer(
            "⚠️ Для вывода необходимо установить username."
        )

        return

    amount = WITHDRAW_AMOUNTS[
        message.text
    ]

    balance = await get_balance(
        message.from_user.id
    )

    if balance < amount:

        await message.answer(
            "❌ У вас недостаточно звёзд для вывода."
        )

        return

    await remove_balance(
        message.from_user.id,
        amount
    )

    await message.answer(
        "✅ Вы успешно отправили заявку на вывод.\n\n"
        "🎁 Подарок придёт вам в течение 16 часов.",
        reply_markup=main_menu
    )


@router.message(
    F.text == "⬅️ Назад"
)
async def back(
    message: Message
):
    await message.answer(
        "Главное меню",
        reply_markup=main_menu
    )
