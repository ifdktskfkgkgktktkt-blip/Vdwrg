# handlers/promocodes.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import (
    add_balance
)

router = Router()

# Пример промокодов
PROMOCODES = {
    "START": {
        "reward": 2,
        "users": []
    },
    "BONUS": {
        "reward": 5,
        "users": []
    }
}


class PromoState(StatesGroup):
    waiting_code = State()


@router.message(
    F.text == "🎟 Промокод"
)
async def promocode_menu(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        PromoState.waiting_code
    )

    await message.answer(
        "🎟 Введите промокод:"
    )


@router.message(
    PromoState.waiting_code
)
async def activate_promocode(
    message: Message,
    state: FSMContext
):
    code = (
        message.text
        .strip()
        .upper()
    )

    user_id = message.from_user.id

    if code not in PROMOCODES:

        await message.answer(
            "❌ Промокод не найден."
        )

        await state.clear()

        return

    if user_id in PROMOCODES[code]["users"]:

        await message.answer(
            "❌ Вы уже использовали этот промокод."
        )

        await state.clear()

        return

    reward = PROMOCODES[code]["reward"]

    PROMOCODES[code]["users"].append(
        user_id
    )

    await add_balance(
        user_id,
        reward
    )

    await message.answer(
        "✅ Промокод успешно активирован!\n\n"
        f"⭐ Вам начислено {reward} звёзд на баланс."
    )

    await state.clear()