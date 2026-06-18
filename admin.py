# keyboards/admin.py

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="⚙️ Изменить награду за реферала"
            )
        ],
        [
            KeyboardButton(
                text="➕ Добавить канал"
            ),
            KeyboardButton(
                text="➖ Удалить канал"
            )
        ],
        [
            KeyboardButton(
                text="📋 Список каналов"
            )
        ],
        [
            KeyboardButton(
                text="💰 Выдать звёзды"
            ),
            KeyboardButton(
                text="❌ Забрать звёзды"
            )
        ],
        [
            KeyboardButton(
                text="🎟 Создать промокод"
            ),
            KeyboardButton(
                text="🗑 Удалить промокод"
            )
        ],
        [
            KeyboardButton(
                text="🎁 Изменить ежедневный бонус"
            )
        ],
        [
            KeyboardButton(
                text="📊 Статистика"
            )
        ],
        [
            KeyboardButton(
                text="📢 Рассылка"
            )
        ],
        [
            KeyboardButton(
                text="👥 Список пользователей"
            )
        ],
        [
            KeyboardButton(
                text="⬅️ Назад"
            )
        ]
    ],
    resize_keyboard=True
)