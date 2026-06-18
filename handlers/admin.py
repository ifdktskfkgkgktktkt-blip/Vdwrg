# handlers/admin.py

from aiogram import Router, F
from aiogram.types import Message

from config import ADMIN_ID
from keyboards.admin import admin_menu

from database import (
    get_users_count,
    add_balance,
    remove_balance,
    add_channel,
    remove_channel,
    get_channels
)

router = Router()

give_mode = {}
take_mode = {}
add_channel_mode = {}
remove_channel_mode = {}
broadcast_mode = {}


@router.message(F.text == "/admin")
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "👑 Админ-панель",
        reply_markup=admin_menu
    )


@router.message(F.text == "📊 Статистика")
async def statistics(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    users = await get_users_count()

    text = (
        "📊 Статистика\n\n"
        f"👥 Всего пользователей: {users}\n"
    )

    await message.answer(text)


@router.message(F.text == "➕ Добавить канал")
async def add_channel_start(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    add_channel_mode[message.from_user.id] = True

    await message.answer(
        "Отправьте username канала\n\n"
        "Пример:\n@channel"
    )


@router.message()
async def add_channel_process(message: Message):

    if message.from_user.id not in add_channel_mode:
        return

    channel = message.text.strip()

    await add_channel(channel)

    del add_channel_mode[
        message.from_user.id
    ]

    await message.answer(
        f"✅ Канал {channel} добавлен"
    )


@router.message(F.text == "➖ Удалить канал")
async def remove_channel_start(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    remove_channel_mode[
        message.from_user.id
    ] = True

    await message.answer(
        "Отправьте канал для удаления"
    )


@router.message()
async def remove_channel_process(message: Message):

    if message.from_user.id not in remove_channel_mode:
        return

    channel = message.text.strip()

    await remove_channel(channel)

    del remove_channel_mode[
        message.from_user.id
    ]

    await message.answer(
        f"✅ Канал {channel} удалён"
    )


@router.message(F.text == "📋 Список каналов")
async def channels_list(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    channels = await get_channels()

    if not channels:

        await message.answer(
            "Список каналов пуст"
        )

        return

    text = "📋 Каналы\n\n"

    for channel in channels:
        text += f"{channel[0]}\n"

    await message.answer(text)


@router.message(F.text == "💰 Выдать звёзды")
async def give_balance_start(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    give_mode[
        message.from_user.id
    ] = True

    await message.answer(
        "Введите:\n\n"
        "ID СУММА\n\n"
        "Пример:\n"
        "123456789 10"
    )


@router.message()
async def give_balance_process(message: Message):

    if message.from_user.id not in give_mode:
        return

    try:

        user_id, amount = (
            message.text.split()
        )

        user_id = int(user_id)
        amount = float(amount)

        await add_balance(
            user_id,
            amount
        )

        del give_mode[
            message.from_user.id
        ]

        await message.answer(
            "✅ Звёзды выданы"
        )

    except:

        await message.answer(
            "Ошибка формата"
        )


@router.message(F.text == "❌ Забрать звёзды")
async def take_balance_start(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    take_mode[
        message.from_user.id
    ] = True

    await message.answer(
        "Введите:\n\n"
        "ID СУММА"
    )


@router.message()
async def take_balance_process(message: Message):

    if message.from_user.id not in take_mode:
        return

    try:

        user_id, amount = (
            message.text.split()
        )

        user_id = int(user_id)
        amount = float(amount)

        await remove_balance(
            user_id,
            amount
        )

        del take_mode[
            message.from_user.id
        ]

        await message.answer(
            "✅ Звёзды списаны"
        )

    except:

        await message.answer(
            "Ошибка формата"
        )


@router.message(F.text == "📢 Рассылка")
async def broadcast_start(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    broadcast_mode[
        message.from_user.id
    ] = True

    await message.answer(
        "Отправьте текст рассылки"
    )
