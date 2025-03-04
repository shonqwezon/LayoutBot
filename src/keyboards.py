from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import src.messages as msg

ownerKb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=msg.DOWNLOAD)],
    ],
    resize_keyboard=True,
)


def get_gb_kb(doc_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text=msg.GOOD, callback_data=f"answer_good_{doc_id}"),
        InlineKeyboardButton(text=msg.BAD, callback_data=f"answer_bad_{doc_id}"),
    )
    return keyboard.as_markup()
