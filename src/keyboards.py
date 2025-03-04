from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

import src.messages as msg

ownerKb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=msg.DOWNLOAD)],
    ],
    resize_keyboard=True,
)
