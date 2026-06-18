# keyboards/user.py

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="⭐ Заработать звёзды"
            ),
            KeyboardButton(
                text="📤 Вывести звёзды"
            )
        ],
        [
            KeyboardButton(
                text="👤 Мой профиль"
            ),
            KeyboardButton(
                text="🎁 Бонус"
            )
        ],
        [
            KeyboardButton(
                text="🎟 Промокод"
            ),
            KeyboardButton(
                text="🏆 Топ рефералов"
            )
        ]
    ],
    resize_keyboard=True
)


withdraw_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="⭐ 15"),
            KeyboardButton(text="⭐ 25")
        ],
        [
            KeyboardButton(text="⭐ 50"),
            KeyboardButton(text="⭐ 100")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
    resize_keyboard=True
)


back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="⬅️ Назад"
            )
        ]
    ],
    resize_keyboard=True
)


def subscribe_keyboard(channels):
    buttons = []

    for channel in channels:
        channel_name = channel[0]

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"⭐ {channel_name}",
                    url=f"https://t.me/{channel_name.replace('@', '')}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ Я подписался",
                callback_data="check_sub"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )