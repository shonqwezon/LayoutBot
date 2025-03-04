from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import src.messages as msg
from src.utils import setup_logger

logger = setup_logger(__name__)
owner = Router()


@owner.message(F.data == "Выгрузить")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    message.answer("OK")
