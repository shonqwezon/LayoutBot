import os
from enum import Enum

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    InputMediaDocument,
    Message,
)

import src.messages as msg
from src.db import export_data
from src.filters import OwnerFilter
from src.utils import setup_logger

logger = setup_logger(__name__)
owner = Router()

owner.message.filter(OwnerFilter())


class Modes(Enum):
    GOOD = "good_data.json", "$gt"
    BAD = "bad_data.json", "$lt"
    EQUAL = "equal_data.json", "$eq"


@owner.message(F.text == msg.DOWNLOAD)
async def download(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Датасет готовится...")

    media_group = []
    for mode in Modes:
        await export_data(mode.value)
        media_group.append(InputMediaDocument(media=FSInputFile(mode.value[0])))
    await message.bot.send_media_group(chat_id=message.from_user.id, media=media_group)

    for mode in Modes:
        os.remove(mode.value[0])
